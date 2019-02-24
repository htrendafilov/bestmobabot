"""
Node.js & heroes.js interface.
"""

from __future__ import annotations

import subprocess
from typing import Any, List, Optional

import ujson as json
from loguru import logger

from bestmobabot.constants import NODEJS_TIMEOUT
from bestmobabot.enums import HeroesJSMode
from bestmobabot.resources import get_heroes_js, get_raw_library, get_skills_sc


def execute_battles(battles_data: List[Any], mode: HeroesJSMode) -> Any:
    footer = FOOTER.format(
        battles_data=json.dumps(battles_data),
        skills_sc=get_skills_sc(),
        library=get_raw_library(),
        mode=mode.value,
    )
    output = run_script(f'{HEADER}{get_heroes_js()}{footer}')
    return json.loads(output) if output else None


def run_script(script: str) -> Optional[str]:
    logger.info('Running Node.js…')
    try:
        process = subprocess.run(
            ['node'],
            input=script,
            encoding='utf-8',
            timeout=NODEJS_TIMEOUT,
            capture_output=True,
        )
    except subprocess.TimeoutExpired:
        logger.error('Timeout expired.')
        return None
    logger.info('Return code: {}.', process.returncode)
    if process.returncode:
        logger.error('Node.js error:\n{}', process.stderr)
        return None
    return process.stdout.rstrip()


HEADER = '''
var window = {
    document: {
        createElement: function() {
            return {
                getContext: function() {
                    return {
                        fillRect: function() {},
                    };
                },
            };
        },
    },
    navigator: {
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
    },
    performance: require('perf_hooks').performance,
};
'''  # noqa

FOOTER = '''
(function(h) {{
    var Bytes = h['haxe.io.Bytes'];
    var BattleInstantPlay = h['game.battle.controller.instant.BattleInstantPlay'];
    var BattlePresets = h['game.battle.controller.thread.BattlePresets'];
    var DataStorage = h['game.data.storage.DataStorage'];
    var AssetStorage = h['game.assets.storage.AssetStorage'];
    var BattleAssetStorage = h['game.assets.storage.BattleAssetStorage'];
    var BattleLog = h['battle.BattleLog'];

    new DataStorage({library});

    AssetStorage.battle = new BattleAssetStorage();
    AssetStorage.battle.loadEncodedCode(new Bytes({skills_sc}));

    var presets = new BattlePresets(false, false, true, DataStorage.battleConfig.get_{mode}(), false);

    var results = [];
    var battles_data = {battles_data};
    for (var i = 0; i < battles_data.length; i++) {{
        // Disable Pako.
        BattleLog.m.bytes.getEncodedString = function() {{ return this.bytes }};

        var play = new BattleInstantPlay(battles_data[i], presets);

        play.battleData.attackers.initialize(AssetStorage.battle.skillFactory.bind(AssetStorage.battle));
        play.battleData.defenders.initialize(AssetStorage.battle.skillFactory.bind(AssetStorage.battle));

        play.executeBattle();
        play.createResult();

        var result = play.get_result();
        results.push({{
            result: result.get_result(),
            progress: result.get_progress(),
        }});
    }}

    console.log(JSON.stringify(results));
}})(window.h)
'''