"""
Arena battle prediction model.
Auto-generated on 2018-03-05 23:59:39.
X shape: (264, 117).
Score: 0.7952 (std: 0.0482).
"""

import pickle

from sklearn.ensemble.forest import RandomForestClassifier

feature_names = ['color_1', 'color_10', 'color_11', 'color_12', 'color_13', 'color_14', 'color_15', 'color_16', 'color_17', 'color_18', 'color_19', 'color_2', 'color_20', 'color_21', 'color_22', 'color_23', 'color_25', 'color_26', 'color_27', 'color_28', 'color_29', 'color_3', 'color_30', 'color_31', 'color_32', 'color_33', 'color_34', 'color_35', 'color_36', 'color_37', 'color_38', 'color_39', 'color_4', 'color_40', 'color_5', 'color_6', 'color_7', 'color_8', 'color_9', 'level_1', 'level_10', 'level_11', 'level_12', 'level_13', 'level_14', 'level_15', 'level_16', 'level_17', 'level_18', 'level_19', 'level_2', 'level_20', 'level_21', 'level_22', 'level_23', 'level_25', 'level_26', 'level_27', 'level_28', 'level_29', 'level_3', 'level_30', 'level_31', 'level_32', 'level_33', 'level_34', 'level_35', 'level_36', 'level_37', 'level_38', 'level_39', 'level_4', 'level_40', 'level_5', 'level_6', 'level_7', 'level_8', 'level_9', 'star_1', 'star_10', 'star_11', 'star_12', 'star_13', 'star_14', 'star_15', 'star_16', 'star_17', 'star_18', 'star_19', 'star_2', 'star_20', 'star_21', 'star_22', 'star_23', 'star_25', 'star_26', 'star_27', 'star_28', 'star_29', 'star_3', 'star_30', 'star_31', 'star_32', 'star_33', 'star_34', 'star_35', 'star_36', 'star_37', 'star_38', 'star_39', 'star_4', 'star_40', 'star_5', 'star_6', 'star_7', 'star_8', 'star_9']