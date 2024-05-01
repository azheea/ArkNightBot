
#版本1.0
import os
import re
import requests
import json
import pickle
#from user import user
import time

import botpy
from botpy import logging

from botpy.message import DirectMessage
from botpy.types.message import Reference
from botpy.message import Message
from botpy.ext.cog_yaml import read

#---------配置---------

server_ip = "http://"

gmkey = ""

console_token_mode = 4 #使用控制台执行命令的身份组权限 1-全体成员 2-管理员 4-频道创建者 5-子频道管理员

console_token_use = True #允许频道主等身份组使用控制台执行命令，默认开启

customcommand = {" 解锁地图":"prop um 1"," 治疗":"h"}#自定义命令

white_channal = ["156372398","136059975"]

#----------------------

useruid = {"null":"null",}

all_character = {'Lancet-2': 'char_285_medic2', 'Castle-3': 'char_286_cast3', 'THRM-EX': 'char_376_therex', '正义骑士号': 'char_4000_jnight', '夜刀': 'char_502_nblade', '黑角': 'char_500_noirc', '巡林者': 'char_503_rang', '杜林': 'char_501_durin', '12F': 'char_009_12fce', '芬': 'char_123_fang', '香草': 'char_240_wyvern', '翎羽': 'char_192_falco', '玫兰莎': 'char_208_melan', '卡缇': 'char_209_ardign', '米格鲁': 'char_122_beagle', '克洛丝': 'char_124_kroos', '安德切尔': 'char_211_adnach', '炎熔': 'char_121_lava', '芙蓉': 'char_120_hibisc', '安赛尔': 'char_212_ansel', '史都华德': 'char_210_stward', '梓兰': 'char_278_orchid', ' 空爆': 'char_282_catap', '月见夜': 'char_283_midn', '斑点': 'char_284_spot', '泡普卡': 'char_281_popka', '夜烟': 'char_141_nights', '远山': 'char_109_fmout', '杰西卡': 'char_235_jesica', '流星': 'char_126_shotst', '白雪': 'char_118_yuki', '讯使': 'char_198_blackd', '清道夫': 'char_149_scave', '红豆': 'char_290_vigna', '杜宾': 'char_130_doberm', '缠丸': 'char_289_gyuki', '霜叶': 'char_193_frostl', '艾丝黛尔': 'char_127_estell', '慕斯': 'char_185_frncat', '砾': 'char_237_gravel', '暗索': 'char_236_rope', '末药': 'char_117_myrrh', '嘉维尔': 'char_187_ccheal', '调香师': 'char_181_flower', '角峰': 'char_199_yak', '蛇屠箱': 'char_150_snakek', '古米': 'char_196_sunbr', '深海色': 'char_110_deepcl', '地灵': 'char_183_skgoat', '阿消': 'char_277_sqrrel', '猎蜂': 'char_137_brownb', '格雷伊': 'char_253_greyy', '桃金娘': 'char_151_myrtle', '苏苏洛': 'char_298_susuro', '坚雷': 'char_260_durnar', '伊桑': 'char_355_ethan', '红云': 'char_190_clour', '梅': 'char_133_mm', '安比尔': 'char_302_glaze', '清流': 'char_385_finlpp', '宴': 'char_337_utage', '刻刀': 'char_301_cutter', '波登可': 'char_258_podego', '卡 达': 'char_328_cammou', '孑': 'char_272_strong', '酸糖': 'char_366_acdrop', '芳汀': 'char_271_spikes', '泡泡': 'char_381_bubble', '杰克': 'char_347_jaksel', '松果': 'char_440_pinecn', '豆苗': 'char_452_bstalk', '深靛': 'char_469_indigo', '罗比菈 塔': 'char_484_robrta', '布丁': 'char_4004_pudd', '褐果': 'char_4041_chnut', '白面鸮': 'char_128_plosis', '凛冬': 'char_115_headbr', '德克萨斯': 'char_102_texas', '芙兰卡': 'char_106_franka', '因陀罗': 'char_155_tiger', '拉普兰德': 'char_140_whitew', '幽灵鲨': 'char_143_ghost', '蓝毒': 'char_129_bluep', '白金': 'char_204_platnm', '陨星': 'char_219_meteo', '阿米娅': 'char_002_amiya', '天火': 'char_166_skfire', '梅尔': 'char_242_otter', '赫默': 'char_108_silent', '华法琳': 'char_171_bldsk', '临光': 'char_148_nearl', '红': 'char_144_red', '雷蛇': 'char_107_liskam', '可颂': 'char_201_moeshd', '火神': 'char_163_hpsts', '普罗旺斯': 'char_145_prove', '守林人': 'char_158_milu', '崖心': 'char_173_slchan', '初雪': 'char_174_slbell', '真理': 'char_195_glassb', '空': 'char_101_sora', '狮蝎': 'char_215_mantic', '食铁兽': 'char_241_panda', '格拉尼': 'char_220_grani', '夜魔': 'char_164_nightm', '诗怀雅': 'char_308_swire', '星极': 'char_274_astesi', '锡兰': 'char_348_ceylon', '格劳克斯': 'char_326_glacus', '微风': 'char_275_breeze', '炎客': 'char_131_flameb', '送葬人': 'char_279_excu', '苇草': 'char_261_sddrag', '布洛卡': 'char_356_broca', '槐琥': 'char_243_waaifu', '拜松': 'char_325_bison', '灰喉': 'char_367_swllow', '吽': 'char_226_hmau', '雪雉': 'char_383_snsant', '惊蛰': 'char_306_leizi', '慑砂': 'char_379_sesa', '柏喙': 'char_252_bibeak', ' 暴行': 'char_230_savage', '巫恋': 'char_254_vodfox', '铸铁': 'char_333_sidero', '极境': 'char_401_elysm', '石棉': 'char_378_asbest', '月禾': 'char_343_tknogi', '苦艾': 'char_405_absin', '莱恩哈特': 'char_373_lionhd', '断崖': 'char_294_ayer', '亚 叶': 'char_345_folnic', '蜜蜡': 'char_344_beewax', '贾维': 'char_349_chiave', '稀音': 'char_336_folivo', '安哲拉': 'char_218_cuttle', '特米米': 'char_411_tomimi', '燧石': 'char_415_flint', '四月': 'char_365_aprl', '薄绿': 'char_388_mint', '奥斯塔': 'char_346_aosta', '鞭刃': 'char_265_sophia', '絮雨': 'char_436_whispr', '卡夫卡': 'char_214_kafka', '罗宾': 'char_451_robin', '爱丽丝': 'char_338_iris', '图耶': 'char_402_tuye', '乌有': 'char_455_nothin', '炎狱炎熔': 'char_1011_lava2', '闪击': 'char_457_blitz', '霜华': 'char_458_rfrost', '战车': 'char_459_tachak', '熔泉': 'char_363_toddi', '暴雨': 'char_304_zebra', '赤冬': 'char_475_akafyu', '绮良': 'char_478_kirara', '贝娜': 'char_369_bena', '羽毛笔': 'char_421_crow', '龙舌兰': 'char_486_takila', '桑葚': 'char_473_mberry', '灰毫': 'char_431_ashlok', '蜜莓': 'char_449_glider', '野鬃': 'char_496_wildmn', '蚀清': 'char_489_serum', '极光': 'char_422_aurora', '耶拉': 'char_4013_kjera', '暮落': 'char_4025_aprot2', '夜半': 'char_476_blkngt', '夏栎': 'char_492_quercu', '寒芒克洛丝': 'char_1021_kroos2', '风丸': 'char_4016_kazema', '见行者': 'char_4036_forcer', '洛洛': 'char_4040_rockr', '海蒂': 'char_4045_heidi', '能天使': 'char_103_angel', '推进之王': 'char_112_siege', '伊 芙利特': 'char_134_ifrit', '艾雅法拉': 'char_180_amgoat', '安洁莉娜': 'char_291_aglina', '闪灵': 'char_147_shining', '夜莺': 'char_179_cgbird', '星熊': 'char_136_hsguma', '塞雷娅': 'char_202_demkni', '银灰': 'char_172_svrash', '斯卡蒂': 'char_263_skadi', '陈': 'char_010_chen', '黑': 'char_340_shwaz', '赫拉格': 'char_188_helage', '麦哲伦': 'char_248_mgllan', '莫斯提马': 'char_213_mostma', '阿': 'char_225_haak', '年': 'char_2014_nian', '煌': 'char_017_huang', '刻俄柏': 'char_2013_cerber', '风笛': 'char_222_bpipe', '傀影': 'char_250_phatom', '温蒂': 'char_400_weedy', 'W': 'char_113_cqbw', '早露': 'char_197_poca', '铃兰': 'char_358_lisa', '棘刺': 'char_293_thorns', '森蚺': 'char_416_zumama', '史尔特尔': 'char_350_surtr', '瑕光': 'char_423_blemsh', '迷迭香': 'char_391_rosmon', '泥岩': 'char_311_mudrok', '山': 'char_264_f12yin', '空弦': 'char_332_archet', '夕': 'char_2015_dusk', '嵯峨': 'char_362_saga', '灰烬': 'char_456_ash', '异客': 'char_472_pasngr', '浊心斯卡蒂': 'char_1012_skadi2', '凯尔希': 'char_003_kalts', '歌蕾蒂娅': 'char_474_glady', '卡涅利安': 'char_426_billro', '帕拉斯': 'char_485_pallas', '假日威龙陈': 'char_1013_chen2', '水月': 'char_437_mizuki', '远牙': 'char_430_fartth', '琴柳': 'char_479_sleach', ' 耀骑士临光': 'char_1014_nearl2', '焰尾': 'char_420_flamtl', '灵知': 'char_206_gnosis', '老鲤': 'char_322_lmlee', '澄闪': 'char_377_gdglow', '令': 'char_2023_ling'}

all_item_type = {'5001': 'EXP_PLAYER', 'SOCIAL_PT': 'SOCIAL_PT', 'AP_GAMEPLAY': 'AP_GAMEPLAY', '6001': 'TKT_TRY', 'base_ap': 'AP_BASE', 'bilibili001': 'TKT_GACHA_PRSV', '4002': 'DIAMOND', '4003': 'DIAMOND_SHD', '3141': 'MATERIAL', '4001': 'GOLD', '3003': 'MATERIAL', '4004': 'HGG_SHD', '4005': 'LGG_SHD', '4006': 'MATERIAL', 'LMTGS_COIN_601': 'LMTGS_COIN', 'LMTGS_COIN_903': 'LMTGS_COIN', 'LMTGS_COIN_1401': 'LMTGS_COIN', 'LMTGS_COIN_1601': 'LMTGS_COIN', 'LMTGS_COIN_1803': 'LMTGS_COIN', 'LMTGS_COIN_2101': 'LMTGS_COIN', 'LMTGS_COIN_2301': 'LMTGS_COIN', 'LMTGS_COIN_2501': 'LMTGS_COIN', 'EPGS_COIN': 'EPGS_COIN', 'REP_COIN': 'REP_COIN', 'CRISIS_SHOP_COIN': 'CRS_SHOP_COIN', 'STORY_REVIEW_COIN': 'MATERIAL', 'RETRO_COIN': 'RETRO_COIN', 'renamingCard': 'RENAMING_CARD', 'renamingCard_0_018': 'RENAMING_CARD', 'renamingCard_30_018': 'RENAMING_CARD', 'renamingCard_0_023': 'RENAMING_CARD', 'renamingCard_30_023': 'RENAMING_CARD', 'ap_supply_lt_100': 'AP_SUPPLY', 'ap_supply_lt_60': 'AP_SUPPLY', 'ap_supply_lt_010': 'AP_SUPPLY', 'ap_supply_lt_100_2022_1': 'AP_SUPPLY', 'ap_supply_lt_100_2022_2': 'AP_SUPPLY', 'ap_supply_lt_100_2022_3': 'AP_SUPPLY', 'ap_supply_lt_100_2022_4': 'AP_SUPPLY', 'ap_supply_lt_100_2022_5': 'AP_SUPPLY', '7004': 'TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_903': 'LIMITED_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_1401': 'LIMITED_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_1601': 'LIMITED_TKT_GACHA_10', 'LINKAGE_TKT_GACHA_10_1701': 'LINKAGE_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_1803': 'LIMITED_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_2101': 'LIMITED_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_2301': 'LIMITED_TKT_GACHA_10', 'LIMITED_TKT_GACHA_10_2501': 'LIMITED_TKT_GACHA_10', '7003': 'TKT_GACHA', '7001': 'TKT_RECRUIT', '7002': 'TKT_INST_FIN', 'voucher_item_4pick1': 'VOUCHER_PICK', 'voucher_item_4pick1_1803': 'VOUCHER_PICK', 'voucher_recruitR5_pick2': 'VOUCHER_PICK', 'voucher_recruitR5_pick1803': 'VOUCHER_PICK', 'voucher_item_pick601': 'VOUCHER_PICK', 'voucher_item_pick1401': 'VOUCHER_PICK', 'voucher_item_pick1803': 'VOUCHER_PICK', 'voucher_item_pick2301': 'VOUCHER_PICK', 'voucher_elite_II_5': 'VOUCHER_ELITE_II_5', 'voucher_skin': 'VOUCHER_SKIN', '2020recruitment10_1': 'VOUCHER_CGACHA', '2020recruitment10_2': 'VOUCHER_CGACHA', '2020recruitment10_3': 'VOUCHER_CGACHA', '2021recruitment10_1': 'VOUCHER_CGACHA', '2021recruitment10_2': 'VOUCHER_CGACHA', '2021recruitment10_3': 'VOUCHER_CGACHA', '2022recruitment10_1': 'VOUCHER_CGACHA', '2022recruitment10_2': 'VOUCHER_CGACHA', '2022recruitment10_3': 'VOUCHER_CGACHA', 'voucher_recruitR4_1': 'VOUCHER_PICK', 'voucher_recruitR3_1': 'VOUCHER_PICK', 'randomMaterialRune_0': 'VOUCHER_MGACHA', 'randomMaterialRune_1': 'VOUCHER_MGACHA', 'randomMaterialRune_2': 'VOUCHER_MGACHA', 'randomMaterialRune_3': 'VOUCHER_MGACHA', 'randomMaterialRune_4': 'VOUCHER_MGACHA', 'randomMaterialRune_5': 'VOUCHER_MGACHA', 'randomMaterialRune_6': 'VOUCHER_MGACHA', 'randomMaterialRune_7': 'VOUCHER_MGACHA', 'randomMaterial_1': 'VOUCHER_MGACHA', 'randomMaterial_2': 'VOUCHER_MGACHA', 'randomMaterial_3': 'VOUCHER_MGACHA', 'randomMaterial_4': 'VOUCHER_MGACHA', 'randomMaterial_5': 'VOUCHER_MGACHA', 'randomDiamondShd_1': 'VOUCHER_MGACHA', 'randomDiamondShd_2': 'VOUCHER_MGACHA', '2001': 'CARD_EXP', '2002': 'CARD_EXP', '2003': 'CARD_EXP', '2004': 'CARD_EXP', '3301': 'MATERIAL', '3302': 'MATERIAL', '3303': 'MATERIAL', 'mod_unlock_token': 'MATERIAL', '30011': 'MATERIAL', '30012': 'MATERIAL', '30013': 'MATERIAL', '30014': 'MATERIAL', '30061': 'MATERIAL', '30062': 'MATERIAL', '30063': 'MATERIAL', '30064': 'MATERIAL', '30031': 'MATERIAL', '30032': 'MATERIAL', '30033': 'MATERIAL', '30034': 'MATERIAL', '30021': 'MATERIAL', '30022': 'MATERIAL', '30023': 'MATERIAL', '30024': 'MATERIAL', '30041': 'MATERIAL', '30042': 'MATERIAL', '30043': 'MATERIAL', '30044': 'MATERIAL', '30051': 'MATERIAL', '30052': 'MATERIAL', '30053': 'MATERIAL', '30054': 'MATERIAL', '30073': 'MATERIAL', '30074': 'MATERIAL', '30083': 'MATERIAL', '30084': 'MATERIAL', '30093': 'MATERIAL', '30094': 'MATERIAL', '30103': 'MATERIAL', '30104': 'MATERIAL', '30115': 'MATERIAL', '30125': 'MATERIAL', '30135': 'MATERIAL', '31013': 'MATERIAL', '31014': 'MATERIAL', '31023': 'MATERIAL', '31024': 'MATERIAL', '31033': 'MATERIAL', '31034': 'MATERIAL', '30145': 'MATERIAL', '31043': 'MATERIAL', '31044': 'MATERIAL', '31053': 'MATERIAL', '31054': 'MATERIAL', '3105': 'MATERIAL', '3401': 'MATERIAL', '3131': 'MATERIAL', '3132': 'MATERIAL', '3133': 'MATERIAL', '3112': 'MATERIAL', '3113': 'MATERIAL', '3114': 'MATERIAL', '32001': 'MATERIAL', '3213': 'MATERIAL', '3223': 'MATERIAL', '3233': 'MATERIAL', '3243': 'MATERIAL', '3253': 'MATERIAL', '3263': 'MATERIAL', '3273': 'MATERIAL', '3283': 'MATERIAL', '3212': 'MATERIAL', '3222': 'MATERIAL', '3232': 'MATERIAL', '3242': 'MATERIAL', '3252': 'MATERIAL', '3262': 'MATERIAL', '3272': 'MATERIAL', '3282': 'MATERIAL', '3211': 'MATERIAL', '3221': 'MATERIAL', '3231': 'MATERIAL', '3241': 'MATERIAL', '3251': 'MATERIAL', '3261': 'MATERIAL', '3271': 'MATERIAL', '3281': 'MATERIAL', 'tier1_pioneer': 'MATERIAL', 'tier1_guard': 'MATERIAL', 'tier1_tank': 'MATERIAL', 'tier1_sniper': 'MATERIAL', 'tier1_caster': 'MATERIAL', 'tier1_medic': 'MATERIAL', 'tier1_supporter': 'MATERIAL', 'tier1_special': 'MATERIAL', 'tier2_pioneer': 'MATERIAL', 'tier2_guard': 'MATERIAL', 'tier2_tank': 'MATERIAL', 'tier2_sniper': 'MATERIAL', 'tier2_caster': 'MATERIAL', 'tier2_medic': 'MATERIAL', 'tier2_supporter': 'MATERIAL', 'tier2_special': 'MATERIAL', 'tier3_pioneer': 'MATERIAL', 'tier3_guard': 'MATERIAL', 'tier3_tank': 'MATERIAL', 'tier3_sniper': 'MATERIAL', 'tier3_caster': 'MATERIAL', 'tier3_medic': 'MATERIAL', 'tier3_supporter': 'MATERIAL', 'tier3_special': 'MATERIAL', 'tier4_pioneer': 'MATERIAL', 'tier4_guard': 'MATERIAL', 'tier4_tank': 'MATERIAL', 'tier4_sniper': 'MATERIAL', 'tier4_caster': 'MATERIAL', 'tier4_medic': 'MATERIAL', 'tier4_supporter': 'MATERIAL', 'tier4_special': 'MATERIAL', 'tier5_pioneer': 'MATERIAL', 'tier5_guard': 'MATERIAL', 'tier5_tank': 'MATERIAL', 'tier5_sniper': 'MATERIAL', 'tier5_caster': 'MATERIAL', 'tier5_medic': 'MATERIAL', 'tier5_supporter': 'MATERIAL', 'tier5_special': 'MATERIAL', 'tier6_pioneer': 'MATERIAL', 'tier6_guard': 'MATERIAL', 'tier6_tank': 'MATERIAL', 'tier6_sniper': 'MATERIAL', 'tier6_caster': 'MATERIAL', 'tier6_medic': 'MATERIAL', 'tier6_supporter': 'MATERIAL', 'tier6_special': 'MATERIAL', 'p_char_285_medic2': 'MATERIAL', 'p_char_286_cast3': 'MATERIAL', 'p_char_376_therex': 'MATERIAL', 'p_char_4000_jnight': 'MATERIAL', 'p_char_502_nblade': 'MATERIAL', 'p_char_500_noirc': 'MATERIAL', 'p_char_503_rang': 'MATERIAL', 'p_char_501_durin': 'MATERIAL', 'p_char_009_12fce': 'MATERIAL', 'p_char_123_fang': 'MATERIAL', 'p_char_240_wyvern': 'MATERIAL', 'p_char_192_falco': 'MATERIAL', 'p_char_208_melan': 'MATERIAL', 'p_char_209_ardign': 'MATERIAL', 'p_char_122_beagle': 'MATERIAL', 'p_char_124_kroos': 'MATERIAL', 'p_char_211_adnach': 'MATERIAL', 'p_char_121_lava': 'MATERIAL', 'p_char_120_hibisc': 'MATERIAL', 'p_char_212_ansel': 'MATERIAL', 'p_char_210_stward': 'MATERIAL', 'p_char_278_orchid': 'MATERIAL', 'p_char_282_catap': 'MATERIAL', 'p_char_283_midn': 'MATERIAL', 'p_char_284_spot': 'MATERIAL', 'p_char_281_popka': 'MATERIAL', 'p_char_141_nights': 'MATERIAL', 'p_char_109_fmout': 'MATERIAL', 'p_char_235_jesica': 'MATERIAL', 'p_char_126_shotst': 'MATERIAL', 'p_char_118_yuki': 'MATERIAL', 'p_char_198_blackd': 'MATERIAL', 'p_char_149_scave': 'MATERIAL', 'p_char_290_vigna': 'MATERIAL', 'p_char_130_doberm': 'MATERIAL', 'p_char_289_gyuki': 'MATERIAL', 'p_char_193_frostl': 'MATERIAL', 'p_char_127_estell': 'MATERIAL', 'p_char_185_frncat': 'MATERIAL', 'p_char_237_gravel': 'MATERIAL', 'p_char_236_rope': 'MATERIAL', 'p_char_117_myrrh': 'MATERIAL', 'p_char_187_ccheal': 'MATERIAL', 'p_char_181_flower': 'MATERIAL', 'p_char_199_yak': 'MATERIAL', 'p_char_150_snakek': 'MATERIAL', 'p_char_196_sunbr': 'MATERIAL', 'p_char_110_deepcl': 'MATERIAL', 'p_char_183_skgoat': 'MATERIAL', 'p_char_277_sqrrel': 'MATERIAL', 'p_char_137_brownb': 'MATERIAL', 'p_char_253_greyy': 'MATERIAL', 'p_char_151_myrtle': 'MATERIAL', 'p_char_298_susuro': 'MATERIAL', 'p_char_260_durnar': 'MATERIAL', 'p_char_355_ethan': 'MATERIAL', 'p_char_190_clour': 'MATERIAL', 'p_char_133_mm': 'MATERIAL', 'p_char_302_glaze': 'MATERIAL', 'p_char_385_finlpp': 'MATERIAL', 'p_char_337_utage': 'MATERIAL', 'p_char_301_cutter': 'MATERIAL', 'p_char_258_podego': 'MATERIAL', 'p_char_328_cammou': 'MATERIAL', 'p_char_272_strong': 'MATERIAL', 'p_char_366_acdrop': 'MATERIAL', 'p_char_271_spikes': 'MATERIAL', 'p_char_381_bubble': 'MATERIAL', 'p_char_347_jaksel': 'MATERIAL', 'p_char_440_pinecn': 'MATERIAL', 'p_char_452_bstalk': 'MATERIAL', 'p_char_469_indigo': 'MATERIAL', 'p_char_484_robrta': 'MATERIAL', 'p_char_4004_pudd': 'MATERIAL', 'p_char_128_plosis': 'MATERIAL', 'p_char_115_headbr': 'MATERIAL', 'p_char_102_texas': 'MATERIAL', 'p_char_106_franka': 'MATERIAL', 'p_char_155_tiger': 'MATERIAL', 'p_char_140_whitew': 'MATERIAL', 'p_char_143_ghost': 'MATERIAL', 'p_char_129_bluep': 'MATERIAL', 'p_char_204_platnm': 'MATERIAL', 'p_char_219_meteo': 'MATERIAL', 'p_char_002_amiya': 'MATERIAL', 'p_char_166_skfire': 'MATERIAL', 'p_char_242_otter': 'MATERIAL', 'p_char_108_silent': 'MATERIAL', 'p_char_171_bldsk': 'MATERIAL', 'p_char_148_nearl': 'MATERIAL', 'p_char_144_red': 'MATERIAL', 'p_char_107_liskam': 'MATERIAL', 'p_char_201_moeshd': 'MATERIAL', 'p_char_163_hpsts': 'MATERIAL', 'p_char_145_prove': 'MATERIAL', 'p_char_158_milu': 'MATERIAL', 'p_char_173_slchan': 'MATERIAL', 'p_char_174_slbell': 'MATERIAL', 'p_char_195_glassb': 'MATERIAL', 'p_char_101_sora': 'MATERIAL', 'p_char_215_mantic': 'MATERIAL', 'p_char_241_panda': 'MATERIAL', 'p_char_220_grani': 'MATERIAL', 'p_char_164_nightm': 'MATERIAL', 'p_char_308_swire': 'MATERIAL', 'p_char_274_astesi': 'MATERIAL', 'p_char_348_ceylon': 'MATERIAL', 'p_char_326_glacus': 'MATERIAL', 'p_char_275_breeze': 'MATERIAL', 'p_char_131_flameb': 'MATERIAL', 'p_char_279_excu': 'MATERIAL', 'p_char_261_sddrag': 'MATERIAL', 'p_char_356_broca': 'MATERIAL', 'p_char_243_waaifu': 'MATERIAL', 'p_char_325_bison': 'MATERIAL', 'p_char_367_swllow': 'MATERIAL', 'p_char_226_hmau': 'MATERIAL', 'p_char_383_snsant': 'MATERIAL', 'p_char_306_leizi': 'MATERIAL', 'p_char_379_sesa': 'MATERIAL', 'p_char_252_bibeak': 'MATERIAL', 'p_char_230_savage': 'MATERIAL', 'p_char_254_vodfox': 'MATERIAL', 'p_char_333_sidero': 'MATERIAL', 'p_char_401_elysm': 'MATERIAL', 'p_char_378_asbest': 'MATERIAL', 'p_char_343_tknogi': 'MATERIAL', 'p_char_405_absin': 'MATERIAL', 'p_char_373_lionhd': 'MATERIAL', 'p_char_294_ayer': 'MATERIAL', 'p_char_345_folnic': 'MATERIAL', 'p_char_344_beewax': 'MATERIAL', 'p_char_349_chiave': 'MATERIAL', 'p_char_336_folivo': 'MATERIAL', 'p_char_218_cuttle': 'MATERIAL', 'p_char_411_tomimi': 'MATERIAL', 'p_char_415_flint': 'MATERIAL', 'p_char_365_aprl': 'MATERIAL', 'p_char_388_mint': 'MATERIAL', 'p_char_346_aosta': 'MATERIAL', 'p_char_265_sophia': 'MATERIAL', 'p_char_436_whispr': 'MATERIAL', 'p_char_214_kafka': 'MATERIAL', 'p_char_451_robin': 'MATERIAL', 'p_char_338_iris': 'MATERIAL', 'p_char_402_tuye': 'MATERIAL', 'p_char_455_nothin': 'MATERIAL', 'p_char_1011_lava2': 'MATERIAL', 'p_char_457_blitz': 'MATERIAL', 'p_char_458_rfrost': 'MATERIAL', 'p_char_459_tachak': 'MATERIAL', 'p_char_363_toddi': 'MATERIAL', 'p_char_304_zebra': 'MATERIAL', 'p_char_475_akafyu': 'MATERIAL', 'p_char_478_kirara': 'MATERIAL', 'p_char_369_bena': 'MATERIAL', 'p_char_421_crow': 'MATERIAL', 'p_char_486_takila': 'MATERIAL', 'p_char_473_mberry': 'MATERIAL', 'p_char_431_ashlok': 'MATERIAL', 'p_char_449_glider': 'MATERIAL', 'p_char_496_wildmn': 'MATERIAL', 'p_char_489_serum': 'MATERIAL', 'p_char_422_aurora': 'MATERIAL', 'p_char_4013_kjera': 'MATERIAL', 'p_char_4025_aprot2': 'MATERIAL', 'p_char_476_blkngt': 'MATERIAL', 'p_char_492_quercu': 'MATERIAL', 'p_char_1021_kroos2': 'MATERIAL', 'p_char_103_angel': 'MATERIAL', 'p_char_112_siege': 'MATERIAL', 'p_char_134_ifrit': 'MATERIAL', 'p_char_180_amgoat': 'MATERIAL', 'p_char_291_aglina': 'MATERIAL', 'p_char_147_shining': 'MATERIAL', 'p_char_179_cgbird': 'MATERIAL', 'p_char_136_hsguma': 'MATERIAL', 'p_char_202_demkni': 'MATERIAL', 'p_char_172_svrash': 'MATERIAL', 'p_char_263_skadi': 'MATERIAL', 'p_char_010_chen': 'MATERIAL', 'p_char_340_shwaz': 'MATERIAL', 'p_char_188_helage': 'MATERIAL', 'p_char_248_mgllan': 'MATERIAL', 'p_char_213_mostma': 'MATERIAL', 'p_char_225_haak': 'MATERIAL', 'p_char_2014_nian': 'MATERIAL', 'p_char_017_huang': 'MATERIAL', 'p_char_2013_cerber': 'MATERIAL', 'p_char_222_bpipe': 'MATERIAL', 'p_char_250_phatom': 'MATERIAL', 'p_char_400_weedy': 'MATERIAL', 'p_char_113_cqbw': 'MATERIAL', 'p_char_197_poca': 'MATERIAL', 'p_char_358_lisa': 'MATERIAL', 'p_char_293_thorns': 'MATERIAL', 'p_char_416_zumama': 'MATERIAL', 'p_char_350_surtr': 'MATERIAL', 'p_char_423_blemsh': 'MATERIAL', 'p_char_391_rosmon': 'MATERIAL', 'p_char_311_mudrok': 'MATERIAL', 'p_char_264_f12yin': 'MATERIAL', 'p_char_332_archet': 'MATERIAL', 'p_char_2015_dusk': 'MATERIAL', 'p_char_362_saga': 'MATERIAL', 'p_char_456_ash': 'MATERIAL', 'p_char_472_pasngr': 'MATERIAL', 'p_char_1012_skadi2': 'MATERIAL', 'p_char_003_kalts': 'MATERIAL', 'p_char_474_glady': 'MATERIAL', 'p_char_426_billro': 'MATERIAL', 'p_char_485_pallas': 'MATERIAL', 'p_char_1013_chen2': 'MATERIAL', 'p_char_437_mizuki': 'MATERIAL', 'p_char_430_fartth': 'MATERIAL', 'p_char_479_sleach': 'MATERIAL', 'p_char_1014_nearl2': 'MATERIAL', 'p_char_420_flamtl': 'MATERIAL', 'p_char_206_gnosis': 'MATERIAL', 'p_char_322_lmlee': 'MATERIAL', 'p_char_377_gdglow': 'MATERIAL', 'p_char_2023_ling': 'MATERIAL', 'voucher_full_ceylon': 'VOUCHER_FULL_POTENTIAL', 'voucher_full_grani': 'VOUCHER_FULL_POTENTIAL', 'voucher_full_flameb': 'VOUCHER_FULL_POTENTIAL', 'voucher_full_bison': 'VOUCHER_FULL_POTENTIAL', 'voucher_full_snsant': 'VOUCHER_FULL_POTENTIAL', 'uni_set_guitar': 'UNI_COLLECTION', 'uni_set_pizza': 'UNI_COLLECTION', 'uni_set_penguin': 'UNI_COLLECTION', 'ap_item_amiya': 'AP_ITEM', 'ap_item_chen': 'AP_ITEM', 'ap_item_texas': 'AP_ITEM', 'ap_item_doberm': 'AP_ITEM', 'ap_item_jesica': 'AP_ITEM', 'ap_item_cast3': 'AP_ITEM', 'ap_item_closure': 'AP_ITEM', 'ap_item_catap': 'AP_ITEM', 'ap_item_blackd': 'AP_ITEM', 'ap_item_slchan': 'AP_ITEM', 'ap_item_SEC_60': 'AP_ITEM', 'ap_item_CaH_200': 'AP_ITEM', 'CRISIS_RUNE_COIN': 'CRS_RUNE_COIN', '1stact': 'ACTIVITY_COIN', 'act1d0_token_gold_rep_1': 'ACTIVITY_ITEM', 'token_Wristband': 'ACTIVITY_ITEM', 'et_ObsidianPass': 'ET_STAGE', 'token_Obsidian': 'ACTIVITY_ITEM', 'token_ObsidianCoin': 'ACTIVITY_ITEM', 'clue_Heavymetal_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_2': 'ACTIVITY_ITEM', 'clue_Heavymetal_3': 'ACTIVITY_ITEM', 'clue_Heavymetal_4': 'ACTIVITY_ITEM', 'clue_Heavymetal_5': 'ACTIVITY_ITEM', 'clue_EDM_1': 'ACTIVITY_ITEM', 'clue_EDM_2': 'ACTIVITY_ITEM', 'clue_EDM_3': 'ACTIVITY_ITEM', 'clue_EDM_4': 'ACTIVITY_ITEM', 'clue_EDM_5': 'ACTIVITY_ITEM', 'clue_Rap_1': 'ACTIVITY_ITEM', 'clue_Rap_2': 'ACTIVITY_ITEM', 'clue_Rap_3': 'ACTIVITY_ITEM', 'clue_Rap_4': 'ACTIVITY_ITEM', 'clue_Rap_5': 'ACTIVITY_ITEM', 'et_ObsidianPass_rep_1': 'ET_STAGE', 'token_Obsidian_rep_1': 'ACTIVITY_ITEM', 'token_ObsidianCoin_rep_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_1_rep_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_2_rep_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_3_rep_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_4_rep_1': 'ACTIVITY_ITEM', 'clue_Heavymetal_5_rep_1': 'ACTIVITY_ITEM', 'clue_EDM_1_rep_1': 'ACTIVITY_ITEM', 'clue_EDM_2_rep_1': 'ACTIVITY_ITEM', 'clue_EDM_3_rep_1': 'ACTIVITY_ITEM', 'clue_EDM_4_rep_1': 'ACTIVITY_ITEM', 'clue_EDM_5_rep_1': 'ACTIVITY_ITEM', 'clue_Rap_1_rep_1': 'ACTIVITY_ITEM', 'clue_Rap_2_rep_1': 'ACTIVITY_ITEM', 'clue_Rap_3_rep_1': 'ACTIVITY_ITEM', 'clue_Rap_4_rep_1': 'ACTIVITY_ITEM', 'clue_Rap_5_rep_1': 'ACTIVITY_ITEM', 'act4d0_intelligencepoint': 'ACTIVITY_ITEM', 'act4d5_point_kfc': 'ACTIVITY_ITEM', 'act5d0_point_medal': 'ACTIVITY_ITEM', 'act5d0_point_medal_rep_1': 'ACTIVITY_ITEM', 'act5d1_point_conbounty': 'ACTIVITY_ITEM', 'act5d1_point_opagrt': 'ACTIVITY_ITEM', 'act6d5_point_firecracker': 'ACTIVITY_ITEM', 'act6d8_point_token': 'ACTIVITY_ITEM', 'act7d5_point_coupon': 'ACTIVITY_ITEM', 'act9d0_token_dogTag': 'ACTIVITY_ITEM', 'act9d0_token_dogTag_rep_1': 'ACTIVITY_ITEM', 'act9d4_point_token': 'ACTIVITY_ITEM', 'act10d5_token_biscuit': 'ACTIVITY_ITEM', 'act11d0_token_currency': 'ACTIVITY_ITEM', 'act11d0_token_currency_rep_1': 'ACTIVITY_ITEM', 'act11d0_token_warrant': 'MATERIAL', 'act12d0_token_components': 'ACTIVITY_ITEM', 'act12d0_token_components_rep_1': 'ACTIVITY_ITEM', 'act12d6_token_mushroom': 'ACTIVITY_ITEM', 'act12d6_token_pancake': 'ACTIVITY_ITEM', 'act13d0_token_dial': 'ACTIVITY_ITEM', 'act13d5_token_securities': 'ACTIVITY_ITEM', 'act13d5_token_securities_rep_1': 'ACTIVITY_ITEM', 'act15d0_token_ironSheet': 'ACTIVITY_ITEM', 'act15d0_token_ironSheet_rep_1': 'ACTIVITY_ITEM', 'act15d5_token_postcard': 'ACTIVITY_ITEM', 'act16d5_token_inker': 'ACTIVITY_ITEM', 'act16d5_token_inker_rep_1': 'ACTIVITY_ITEM', 'act17d0_token_form': 'ACTIVITY_ITEM', 'act18d0_token_page': 'ACTIVITY_ITEM', 'act18d3_token_record': 'ACTIVITY_ITEM', 'act7mini_token_permit': 'ACTIVITY_ITEM', 'act1lock_point_reward': 'ACTIVITY_ITEM', 'act8mini_token_vigilo': 'ACTIVITY_ITEM', 'act12side_token_coupon': 'ACTIVITY_ITEM', 'act12side_point_cmemomedal': 'ACTIVITY_ITEM', 'act12side_token_key01': 'MATERIAL', 'act12side_token_key02': 'MATERIAL', 'act12side_token_key03': 'MATERIAL', 'act12side_token_key04': 'MATERIAL', 'act9mini_token_ticket': 'ACTIVITY_ITEM', 'act13side_token_model': 'ACTIVITY_ITEM', 'act13side_token_key': 'MATERIAL', 'act13side_token_card': 'MATERIAL', 'act13side_prestige_kazimierz': 'MATERIAL', 'act13side_prestige_commerce': 'MATERIAL', 'act13side_prestige_armorless': 'MATERIAL', 'act14side_token_stone': 'ACTIVITY_ITEM', 'rogue_1_token_bp': 'RL_COIN', 'rogue_1_token_grow': 'RL_COIN', 'act10mini_token_ticket': 'ACTIVITY_ITEM', 'act15side_token_tea': 'ACTIVITY_ITEM', 'uni_set_act7d5': 'UNI_COLLECTION', 'return_credit_token': 'RETURN_CREDIT'}

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")


    async def on_at_message_create(self, message: Message):


        message.content = message.content[23:]

        if(message.channel_id in white_channal or "/子频道" in message.content):
            #/帮助命令
            if("/帮助" in message.content):
                backw = "本机器人由啊这.制作\n使用#命令以执行命令,目前支持的修改的有:\n龙门币、(博士)等级、源石、理智、玩家昵称 目前以上功能已暂时停用\n 远程获取角色 物品\n输入/帮助 <命令> 显示帮助"
                if("昵称" in message.content):
                    backw = "使用格式#昵称 <昵称> 暂时停用"
                if("龙门币" in message.content):
                    backw = "使用格式#龙门币 <数量> 暂时停用"
                if("角色" in message.content):
                    backw = "使用格式#角色 <角色id>"
                if("物品" in message.content):
                    backw = "使用格式#物品 <物品id> <数量>"
                if("等级" in message.content):
                    backw = "使用格式#等级 <等级> 暂时停用"
                if("理智" in message.content):
                    backw = "使用格式#理智 <数量> 暂时停用"
                if("全角色" in message.content):
                    backw = "使用格式#全角色"
                if("源石" in message.content):
                    backw = "使用格式#源石 <数量> 暂时停用"

            #/状态命令
            elif("/状态" in message.content ):
                if((json.loads((requests.post(server_ip+"/online/v1/ping", json={"value":"/v1/ping"},verify=False)).text))["message"] == "OK"):
                    backw = "服务器在线!"
                else:
                    backw = "服务器离线!"

            #/状态命令
            elif("/子频道" in message.content ):
                backw = "子频道id为:"+message.channel_id


            #执行命令
            elif(message.content[1] == "#"):
                #提取命令
                player_command = message.content
                if(player_command == ""):
                    player_command ="null"
                if(str(useruid.get(message.author.id, "null")) == "null"):
                    backw = "请先使用/绑定命令"
                else:
                    player_uid = str(useruid.get(message.author.id, "null"))
                    # if("源石" in player_command):
                    #     player_command = message.content.replace('#源石','')
                    #     if(player_command.isdecimal() != True):
                    #         player_command = int(player_command)
                    #         if(player_command <= 999999999):
                    #             user(str(useruid.get(message.author.id, "null"))).setStatus("diamondShard",int(player_command))
                    #             backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的源石设置为"+str(player_command)+"\n重新登录后生效"
                    #         else:
                    #             backw = "数据不合法"
                    #     else:
                    #         backw = "数据不合法"


                    # elif("等级" in player_command):
                    #     player_command = message.content.replace('#等级','')
                    #     print(player_command)
                    #     if(player_command.isdecimal() != True):
                    #         player_command = int(player_command)
                    #         if(player_command <= 120):
                    #             user(str(useruid.get(message.author.id, "null"))).setStatus("level",int(player_command))
                    #             backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的等级设置为"+str(player_command)+"\n重新登录后生效"
                    #         else:
                    #             backw = "数据不合法"
                    #     else:
                    #         backw = "数据不合法"


                    # elif("龙门币" in player_command):
                    #     player_command = message.content.replace('#龙门币','')
                    #     print(player_command)

                    #     if(player_command.isdecimal() != True):
                    #         player_command = int(player_command)
                    #         if(player_command <= 999999999999999999):
                    #             user(str(useruid.get(message.author.id, "null"))).setStatus("gold",int(player_command))
                    #             backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的龙门币设置为"+str(player_command)+"\n重新登录后生效"
                    #         else:
                    #             backw = "数据不合法"
                    #     else:
                    #         backw = "数据不合法"


                    # elif("理智" in player_command):
                    #     player_command = message.content.replace('#理智','')
                    #     print(player_command)
                    #     if(player_command.isdecimal() != True):
                    #         player_command = int(player_command)
                    #         if(player_command <= 999999):
                    #             user(str(useruid.get(message.author.id, "null"))).setStatus("ap",int(player_command))
                    #             backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的理智设置为"+str(player_command)+"\n重新登录后生效"
                    #         else:
                    #             backw = "数据不合法"
                    #     else:
                    #         backw = "数据不合法"


                    # if("昵称" in player_command):
                    #     player_command = message.content.replace('#昵称','')
                    #     player_command = player_command.replace('&lt;','<')
                    #     player_command = player_command.replace('&gt;','>')
                    #     user(str(useruid.get(message.author.id, "null"))).setStatus("nickName",player_command)
                    #     backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的昵称设置为"+str(player_command)+"\n重新登录后生效"


                    if("#角色" in player_command):
                        player_command = message.content.replace('#角色','')
                        player_command = player_command.replace(' ','')
                        for key, value in all_character.items():
                            # Check if the key is in the variable b
                            if key in player_command:
                            # Replace the key with the value
                                player_command = player_command.replace(key, value)
                        headers = {'GMKey': str(gmkey)}
                        params = {
                        'uid': useruid.get(message.author.id, "null"),
                        'charId': player_command
                        }
                        yuanchengip = server_ip+"/admin/send/character"
                        response = requests.get(yuanchengip, headers=headers, params=params)
                        backw = "成功给予" + str(str(useruid.get(message.author.id, "null")))+"玩家角色"+str(player_command)+"\n重新登录后生效"

                    elif("#全角色" in player_command):
                        _message = await message.reply(content="[Arkbot]收到! 已经开始发送! 请其他玩家稍等!",message_reference=Reference(message_id=message.id))
                        cishu = 0
                        for value in all_character.values():
                            headers = {'GMKey': str(gmkey)}
                            params = {
                            'uid': useruid.get(message.author.id, "null"),
                            'charId': value
                            }
                            yuanchengip = server_ip+"/admin/send/character"
                            response = requests.get(yuanchengip, headers=headers, params=params)
                        backw = "已为玩家<@"+str(message.author.id)+">发送全角色 \n重新登录后生效 \n其他玩家可以执行指令了!"

                    elif("物品" in player_command):
                        user_command = player_command.split(' ')
                        if("#物品" in user_command):
                            if (len(user_command)-1 == user_command.index("#物品") or len(user_command)-2  == user_command.index("#物品")):
                                backw = "格式错误 正确格式为#物品 <物品id> <数量>"
                            
                            else:
                                if(user_command[len(user_command)-2] in all_item_type):
                                    headers = {'GMKey': str(gmkey)}
                                    params = {
                                    'uid': useruid.get(message.author.id, "null"),
                                    'itemId': user_command[len(user_command)-2],
                                    'count' : user_command[len(user_command)-1],
                                    'itemType': all_item_type[user_command[len(user_command)-2]]
                                    }
                                    yuanchengip = server_ip+"/admin/send/item"
                                    response = requests.get(yuanchengip, headers=headers, params=params)
                                    backw = "成功给予" + str(str(useruid.get(message.author.id, "null")))+"玩家"+str(user_command[len(user_command)-2])+"\n重新登录后生效"
                                else:
                                    backw = "物品不存在"
                        else:
                            backw = "格式错误 正确格式为#物品 <物品id> <数量>"

                    # elif("重置" in player_command):
                    #     user(str(useruid.get(message.author.id, "null"))).setStatus("ap",0)
                    #     user(str(useruid.get(message.author.id, "null"))).setStatus("gold",0)
                    #     user(str(useruid.get(message.author.id, "null"))).setStatus("level",1)
                    #     user(str(useruid.get(message.author.id, "null"))).setStatus("androidDiamond",0)
                    #     backw = "成功将" + str(str(useruid.get(message.author.id, "null")))+"的状态重置\n重新登录后生效"
                    
                    else:
                        backw = "未知命令"

            #绑定uid
            elif("/绑定" in message.content):
                #提取uid
                player_uid = message.content.replace('/绑定','')
                player_uid = player_uid.replace(' ','')
                if(player_uid == ""):
                    player_uid ="null"
                if(player_uid.isdecimal() == True and len(player_uid) == 8):
                    useruid[message.author.id] = player_uid
                    backw = "绑定uid为"+player_uid
                else:
                    backw = "错误，uid：" + player_uid + "中含有非数字内容或不是标准的8位uid"
                


            #其它的情况？
            else:
                backw = "未知命令，请使用/帮助 获取帮助"

        else:
            backw = "请前往对应子频道执行指令"
        #反馈
        _message = await message.reply(content="[Arkbot]" + str(backw),message_reference=Reference(message_id=message.id))
















if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道 
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
