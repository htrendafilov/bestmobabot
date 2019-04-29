from __future__ import annotations

from orjson import loads
from pytest import mark

from bestmobabot import dataclasses_
from bestmobabot.resources import get_library


def test_library():
    get_library()


@mark.parametrize('response', [
    # language=json
    r'{}',

    # language=json
    '{"consumable":{"24":250}}',

    # language=json
    '{"dungeonActivity": 1,"consumable": {"20": 25}}',

    # language=json
    '{"coin": {"13": "2"}}',

    # language=json
    '{"dungeonActivity":5,"fragmentTitan":{"4012":1}}',
])
def test_reward(response: str):
    dataclasses_.Reward.parse_obj(loads(response)).log()


@mark.parametrize('response', [
    # language=json
    r'{"champions":{"5181775":{"userId":"5181775","place":1,"serverId":"7","clanId":"49207","score":"84229","power":"825499","cup":1,"info":{"name":"Faal","level":"130","avatarId":"386","frameId":3,"clanTitle":"Неудержимые NEW","clanIcon":{"flagColor1":16,"flagColor2":19,"flagShape":1,"iconColor":19,"iconShape":5},"serverId":"7","clanId":"49207"}},"5069714":{"userId":"5069714","place":2,"serverId":"2","clanId":"3980","score":"84210","power":"825436","cup":2,"info":{"name":"Бяка","level":"130","avatarId":"305","frameId":3,"clanTitle":"T-Grad","clanIcon":{"flagColor1":16,"flagColor2":0,"flagShape":1,"iconColor":3,"iconShape":10},"serverId":"2","clanId":"3980"}},"1207246":{"userId":"1207246","place":3,"serverId":"11","clanId":"8050","score":"84147","power":"825436","cup":2,"info":{"name":"isaac morris","level":"130","avatarId":"411","frameId":3,"clanTitle":"BewareUs","clanIcon":{"flagColor1":8,"flagColor2":19,"flagShape":14,"iconColor":7,"iconShape":31},"serverId":"11","clanId":"8050"}},"5176560":{"userId":"5176560","place":4,"serverId":"9","clanId":"23928","score":"84047","power":"825499","cup":2,"info":{"name":"68 RUS","level":"130","avatarId":"305","frameId":3,"clanTitle":"NFS","clanIcon":{"flagColor1":0,"flagColor2":3,"flagShape":14,"iconColor":0,"iconShape":46},"serverId":"9","clanId":"23928"}},"5222351":{"userId":"5222351","place":5,"serverId":"3","clanId":"45148","score":"84018","power":"825499","cup":2,"info":{"name":"Бог смерти Рюк","level":"130","avatarId":"374","frameId":3,"clanTitle":"Revolution","clanIcon":{"flagColor1":0,"flagColor2":19,"flagShape":3,"iconColor":8,"iconShape":2},"serverId":"3","clanId":"45148"}},"5355159":{"userId":"5355159","place":6,"serverId":"7","clanId":"49207","score":"83823","power":"825436","cup":2,"info":{"name":"ЛЕГИОН","level":"130","avatarId":"303","frameId":3,"clanTitle":"Неудержимые NEW","clanIcon":{"flagColor1":16,"flagColor2":19,"flagShape":1,"iconColor":19,"iconShape":5},"serverId":"7","clanId":"49207"}},"4944789":{"userId":"4944789","place":7,"serverId":"17","clanId":"20301","score":"83756","power":"820715","cup":2,"info":{"name":"Катастрофа","level":"130","avatarId":"385","frameId":3,"clanTitle":"Paradox","clanIcon":{"flagColor1":0,"flagColor2":0,"flagShape":14,"iconColor":19,"iconShape":12},"serverId":"17","clanId":"20301"}},"4534638":{"userId":"4534638","place":8,"serverId":"22","clanId":"23965","score":"83736","power":"825499","cup":2,"info":{"name":"М_А_К_С","level":"130","avatarId":"303","frameId":3,"clanTitle":"PROTEX","clanIcon":{"flagColor1":9,"flagColor2":7,"flagShape":0,"iconColor":5,"iconShape":14},"serverId":"22","clanId":"23965"}},"5069879":{"userId":"5069879","place":9,"serverId":"34","clanId":"19945","score":"83705","power":"825499","cup":2,"info":{"name":"Артем","level":"130","avatarId":"385","frameId":3,"clanTitle":"Brazzers","clanIcon":{"flagColor1":19,"flagColor2":19,"flagShape":5,"iconColor":3,"iconShape":27},"serverId":"34","clanId":"19945"}},"5182053":{"userId":"5182053","place":10,"serverId":"5","clanId":"24015","score":"83666","power":"821785","cup":2,"info":{"name":"Моль","level":"130","avatarId":"397","frameId":3,"clanTitle":"E-бобо","clanIcon":{"flagColor1":19,"flagColor2":7,"flagShape":14,"iconColor":19,"iconShape":17},"serverId":"5","clanId":"24015"}}},"bestOnServer":false,"bestGuildMembers":[],"result":{"place":"58774","cup":"5"},"key":1550865600,"next":null,"prev":1549850400,"trophy":{"cup":"5","week":"1550455200","place":"58774","serverId":"10","clanId":"15676","championReward":{"coin":{"19":"2"},"gold":"150000"},"championRewardFarmed":0,"serverReward":[],"serverRewardFarmed":0,"clanReward":[],"clanRewardFarmed":0}}',  # noqa
    # language=json
    r'{"response":{"champions":{"5182053":{"userId":"5182053","place":1,"serverId":"5","clanId":"24015","score":"84379","power":"825436","cup":1,"info":{"name":"\u041c\u043e\u043b\u044c","level":"130","avatarId":"397","frameId":3,"clanTitle":"E-\u0431\u043e\u0431\u043e","clanIcon":{"flagColor1":19,"flagColor2":7,"flagShape":14,"iconColor":19,"iconShape":17},"serverId":"5","clanId":"24015"}},"5164854":{"userId":"5164854","place":2,"serverId":"51","clanId":"39267","score":"84338","power":"825454","cup":2,"info":{"name":"\u0418\u0433\u043e\u0440\u044c \u0427\u0438\u0442\u0438\u043d\u0441\u043a\u0438\u0439","level":"130","avatarId":"386","frameId":3,"clanTitle":"\u041e\u0440\u0434\u0435\u043d \u041b\u044c\u0432\u0438\u043d\u043e\u0435 \u0441\u0435\u0440\u0434\u0446\u0435","clanIcon":{"flagColor1":0,"flagColor2":0,"flagShape":13,"iconColor":3,"iconShape":28},"serverId":"51","clanId":"39267"}},"5069714":{"userId":"5069714","place":3,"serverId":"2","clanId":"3980","score":"84275","power":"825499","cup":2,"info":{"name":"\u0411\u044f\u043a\u0430","level":"130","avatarId":"305","frameId":3,"clanTitle":"T-Grad","clanIcon":{"flagColor1":16,"flagColor2":0,"flagShape":1,"iconColor":3,"iconShape":10},"serverId":"2","clanId":"3980"}},"1207246":{"userId":"1207246","place":4,"serverId":"11","clanId":"8050","score":"84205","power":"825436","cup":2,"info":{"name":"isaac morris","level":"130","avatarId":"430","frameId":3,"clanTitle":"BewareUs","clanIcon":{"flagColor1":8,"flagColor2":19,"flagShape":14,"iconColor":7,"iconShape":31},"serverId":"11","clanId":"8050"}},"5546832":{"userId":"5546832","place":5,"serverId":"7","clanId":"49207","score":"84147","power":"825454","cup":2,"info":{"name":"\u041b\u0415\u0413\u0418\u041e\u041d","level":"130","avatarId":"303","frameId":3,"clanTitle":"\u041d\u0435\u0443\u0434\u0435\u0440\u0436\u0438\u043c\u044b\u0435 NEW","clanIcon":{"flagColor1":16,"flagColor2":19,"flagShape":1,"iconColor":19,"iconShape":5},"serverId":"7","clanId":"49207"}},"5435649":{"userId":"5435649","place":6,"serverId":"1","clanId":"34834","score":"84059","power":"825436","cup":2,"info":{"name":"68 RUS","level":"130","avatarId":"305","frameId":3,"clanTitle":"Song of Blood","clanIcon":{"flagColor1":0,"flagColor2":3,"flagShape":14,"iconColor":0,"iconShape":46},"serverId":"1","clanId":"34834"}},"5069879":{"userId":"5069879","place":7,"serverId":"34","clanId":"19945","score":"83894","power":"825436","cup":2,"info":{"name":"\u0410\u0440\u0442\u0435\u043c","level":"130","avatarId":"385","frameId":3,"clanTitle":"Brazzers","clanIcon":{"flagColor1":19,"flagColor2":19,"flagShape":5,"iconColor":3,"iconShape":27},"serverId":"34","clanId":"19945"}},"4944789":{"userId":"4944789","place":8,"serverId":"17","clanId":"51713","score":"83671","power":"820715","cup":2,"info":{"name":"\u041a\u0430\u0442\u0430\u0441\u0442\u0440\u043e\u0444\u0430","level":"130","avatarId":"385","frameId":2,"clanTitle":"\u0424\u0438\u043e\u043b\u0435\u0442\u043e\u0432\u0435\u043d\u044c\u043a\u043e","clanIcon":{"flagColor1":10,"flagColor2":10,"flagShape":11,"iconColor":11,"iconShape":10},"serverId":"17","clanId":"51713"}},"5443938":{"userId":"5443938","place":9,"serverId":"1","clanId":"197","score":"83527","power":"776275","cup":2,"info":{"name":"\u0422\u0415\u0421\u0415\u0419","level":"130","avatarId":"234","frameId":3,"clanTitle":"CHESS","clanIcon":{"flagColor1":7,"flagColor2":19,"flagShape":1,"iconColor":3,"iconShape":47},"serverId":"1","clanId":"197"}},"5397688":{"userId":"5397688","place":10,"serverId":"3","clanId":"45148","score":"83489","power":"825499","cup":2,"info":{"name":"\u0411\u043e\u0433 \u0441\u043c\u0435\u0440\u0442\u0438 \u0420\u044e\u043a","level":"130","avatarId":"385","frameId":3,"clanTitle":"Revolution","clanIcon":{"flagColor1":0,"flagColor2":19,"flagShape":3,"iconColor":8,"iconShape":2},"serverId":"3","clanId":"45148"}}},"bestOnServer":false,"bestGuildMembers":[],"result":{"place":null,"cup":null},"key":1554494400,"next":null,"prev":1553479200,"trophy":[]}}',  # noqa
])
def test_hall_of_fame(response: str):
    dataclasses_.HallOfFame.parse_obj(loads(response))


@mark.parametrize('response', [
    # language=json
    r'{"userId":"833061","typeId":"4731386","attackers":{"15":{"id":15,"xp":268663,"level":66,"color":8,"slots":{"0":0,"3":0,"4":0,"1":0,"2":0},"skills":{"72":66,"73":66,"74":66,"75":66},"power":14150,"star":4,"runes":[1840,660,0,0,0],"skins":{"15":12},"currentSkin":15,"titanGiftLevel":2,"titanCoinsSpent":{"consumable":{"24":510}},"artifacts":[{"level":6,"star":1},{"level":11,"star":1},{"level":7,"star":1}],"scale":1,"agility":1023,"hp":9445,"intelligence":658,"physicalAttack":1350,"strength":742,"armor":455,"armorPenetration":525,"magicResist":427,"skin":15},"34":{"id":34,"xp":2044637,"level":106,"color":9,"slots":{"2":0,"3":0,"4":0,"0":0,"1":0},"skills":{"170":106,"171":106,"172":106,"173":106},"power":24348,"star":5,"runes":[0,0,0,0,0],"skins":[],"currentSkin":0,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":15,"star":3},{"level":14,"star":2},{"level":15,"star":1}],"scale":1,"agility":1320,"hp":6164.6999999999998,"intelligence":2253,"physicalAttack":78,"strength":1209,"armor":857,"magicPower":2828.5,"magicResist":804,"skin":0},"10":{"id":10,"xp":1393323,"level":95,"color":10,"slots":{"0":0,"4":0,"2":0,"1":0,"3":0},"skills":{"47":95,"48":95,"49":95,"50":95},"power":27104,"star":6,"runes":[650,660,0,0,0],"skins":{"10":10,"66":18},"currentSkin":66,"titanGiftLevel":1,"titanCoinsSpent":{"consumable":{"24":250}},"artifacts":[{"level":20,"star":3},{"level":14,"star":1},{"level":23,"star":2}],"scale":1,"agility":1416,"hp":14505,"intelligence":2633.1999999999998,"physicalAttack":693,"strength":1421,"magicPenetration":945,"magicPower":3860,"magicResist":1235,"skin":66},"37":{"id":37,"xp":3149200,"level":123,"color":11,"slots":{"4":0,"5":0,"0":0,"1":0},"skills":{"185":123,"186":123,"187":123,"188":123},"power":27055,"star":4,"runes":[0,0,0,0,0],"skins":{"83":17},"currentSkin":83,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":12,"star":3},{"level":11,"star":1},{"level":10,"star":2}],"scale":1,"agility":1377,"hp":13990,"intelligence":973,"physicalAttack":2620,"strength":2021.0999999999999,"armor":997,"armorPenetration":1595,"magicResist":595,"physicalCritChance":481,"skin":83},"29":{"id":29,"xp":3625195,"level":130,"color":10,"slots":{"1":0,"4":0,"0":0,"2":0,"3":0},"skills":{"145":130,"146":130,"147":130,"148":130},"power":36552,"star":6,"runes":[0,0,50,0,0],"skins":[],"currentSkin":0,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":50,"star":3},{"level":51,"star":2},{"level":50,"star":2}],"scale":1,"agility":1883,"hp":30241.200000000001,"intelligence":3675.8000000000002,"physicalAttack":106,"strength":2018,"armor":781,"magicPower":3885.8000000000002,"magicResist":747,"skin":0}},"defenders":[{"4":{"id":4,"xp":690174,"level":81,"color":7,"slots":{"0":0,"2":0,"1":0,"3":0},"skills":{"255":32,"256":44,"257":40,"258":73},"power":15886,"star":5,"runes":[900,920,730,0,0],"skins":{"4":21},"currentSkin":4,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":16,"star":3},{"level":15,"star":2},{"level":16,"star":2}],"scale":1,"agility":1010,"hp":10155,"intelligence":1096,"physicalAttack":231,"strength":1549.2,"armor":1078.9000000000001,"magicPower":687,"magicResist":732.89999999999998,"skin":4},"18":{"id":18,"xp":2818582,"level":118,"color":9,"slots":{"1":0,"0":0,"2":0},"skills":{"87":61,"88":80,"89":118,"90":71},"power":33398,"star":6,"runes":[1330,3740,2700,2080,70],"skins":{"18":36},"currentSkin":18,"titanGiftLevel":3,"titanCoinsSpent":{"consumable":{"24":780}},"artifacts":[{"level":61,"star":4},{"level":41,"star":3},{"level":60,"star":3}],"scale":1,"agility":1711,"hp":18608,"intelligence":3953,"physicalAttack":106,"strength":1834,"armor":1810,"magicPower":3494.5999999999999,"magicResist":1512,"skin":18},"37":{"id":37,"xp":1671449,"level":100,"color":9,"slots":{"0":0,"4":0},"skills":{"185":62,"186":35,"187":61,"188":80},"power":18051,"star":4,"runes":[490,840,330,410,840],"skins":{"50":23},"currentSkin":50,"titanGiftLevel":10,"titanCoinsSpent":{"consumable":{"24":5750}},"artifacts":[{"level":16,"star":3},{"level":14,"star":2},{"level":15,"star":2}],"scale":1,"agility":1091,"hp":10950,"intelligence":786,"physicalAttack":1740.5,"strength":1839.4000000000001,"armor":677,"armorPenetration":408,"magicResist":235,"physicalCritChance":240.90000000000001,"skin":50},"15":{"id":15,"xp":1263160,"level":93,"color":9,"slots":{"1":0,"3":0,"0":0,"4":0},"skills":{"72":51,"73":40,"74":42,"75":60},"power":19972,"star":5,"runes":[2700,3220,2760,350,50],"skins":{"15":22,"34":15},"currentSkin":34,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":20,"star":3},{"level":21,"star":2},{"level":16,"star":2}],"scale":1,"agility":1953.2,"hp":16560,"intelligence":1085,"physicalAttack":2378.1999999999998,"strength":1289,"armor":655,"armorPenetration":887.5,"magicResist":1267,"skin":34},"19":{"id":19,"xp":701209,"level":81,"color":8,"slots":{"0":0,"3":0,"1":0,"2":0},"skills":{"92":44,"93":30,"94":41,"95":53},"power":17847,"star":6,"runes":[490,850,330,260,0],"skins":{"19":13},"currentSkin":19,"titanGiftLevel":0,"titanCoinsSpent":null,"artifacts":[{"level":14,"star":2},{"level":14,"star":3},{"level":15,"star":2}],"scale":1,"agility":1979.4000000000001,"hp":8645,"intelligence":1195,"physicalAttack":1019,"strength":1271,"armorPenetration":764,"dodge":263,"magicResist":247,"skin":19}}],"effects":[],"reward":[],"startTime":"1553538054","seed":"1809861544","type":"grand","id":"1553538054871551588","progress":[],"result":{"win":true,"stars":2,"battleOrder":2,"serverVersion":153,"oldPlace":"425","newPlace":"417","enemyPlace":"417"},"endTime":"1553538054"}',  # noqa
])
def test_replay(response: str):
    dataclasses_.Replay.parse_obj(loads(response))


@mark.parametrize('response', [
    # language=json
    r'{"id":15,"xp":256129,"level":66,"color":7,"slots":[0],"skills":{"72":48,"73":48,"74":48,"75":64},"power":10083,"star":3,"runes":[100,0,0,0,0],"skins":[],"currentSkin":0,"titanGiftLevel":1,"titanCoinsSpent":{"consumable":{"24":250}},"artifacts":[{"level":3,"star":1},{"level":10,"star":1},{"level":3,"star":1}],"scale":1}',  # noqa
    # language=json
    r'{"id":7,"level":130,"color":13,"star":5}',
    # language=json
    r'{"id":2,"xp":372120,"level":71,"color":9,"slots":{"1":0,"0":0,"2":0,"3":0,"4":0},"skills":{"270":71,"271":71,"272":71,"273":71},"power":17852,"star":5,"runes":[210,250,10,0,0],"skins":{"2":3},"currentSkin":2,"titanGiftLevel":2,"titanCoinsSpent":{"consumable":{"24":510}},"artifacts":[{"level":15,"star":3},{"level":19,"star":3},{"level":17,"star":2}],"scale":1}',  # noqa
])
def test_hero(response: str):
    dataclasses_.Hero.parse_obj(loads(response))
