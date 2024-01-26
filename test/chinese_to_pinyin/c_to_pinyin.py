# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 18:52
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: c_to_pinyin.py
# @Software: PyCharm
# @User: chent


from pypinyin import lazy_pinyin


def chinese_to_pinyin(chinese_str):
    return ' '.join(lazy_pinyin(chinese_str))


l = ['挖一般土方',
    "挖基坑土石方",
    "回填方",
    "余方弃置",
    "钻孔旋挖灌注桩 Φ800",
    "截（凿）桩头",
    "MU10烧结页岩多孔砖(外墙、楼梯间及厨卫隔墙)",
    "加气混凝土砌块（内墙）",
    "砖基础（地面以下土中的墙体）",
    "垫层 C15",
    "地面垫层 C15",
    "基础梁 C30",
    "桩承台 C30",
    "抗水底板 C30 P6",
    "地下室顶板 C30 P6",
    "挡土墙 C30 P6",
    "消防水池直形墙 C30 P6",
    "直形墙 C40",
    "直形墙 C35",
    "直形墙 C30",
    "框架柱 C30",
    "有梁板 C30",
    "构造柱 C25",
    "圈梁 C25",
    "过梁 C25",
    "矩形梁 C30",
    "空调板、飘窗板、雨棚板 C30",
    "直形楼梯 C30",
    "厨房、卫生间、阳台翻边 C20",
    "细石混凝土 C20",
    "其他构件 C25",
    "集水坑 2000*1500*3400mm",
    "集水坑 1000*1000*1000mm",
    "电梯基坑 2400*2400*2000mm",
    "现浇构件钢筋 圆钢 直径≤φ10",
    "现浇构件钢筋 圆钢 直径φ12～φ16",
    "现浇构件钢筋（螺旋钢筋） 圆钢 直径≤φ10",
    "现浇构件钢筋 Ⅲ级螺纹钢 直径≤φ10",
    "现浇构件钢筋 Ⅲ级螺纹钢  直径φ12～φ16",
    "现浇构件钢筋 Ⅲ级螺纹钢  直径＞φ16",
    "砌体加固钢筋  圆钢 直径≤φ10",
    "预制构件钢筋 圆钢 直径≤φ10",
    "直螺纹套筒连接φ25",
    "砌块墙钢丝网加固（不同材料交界处）",
    "钢质防火防盗门（入户门）",
    "深灰色铝合金推拉门（6中透光Low-E+9氩气+6透明）",
    "塑钢平开窗（6中透光Low-E+9氩气+6透明）",
    "深灰色铝合金平开门M1824",
    "屋面一(倒置式上人保温平屋面)",
    "屋面二(不上人保温屋面)",
    "外墙3 地下室挡墙防水",
    "商铺卫生间楼地面防水",
    "厨房,卫生间,阳台楼地面防水",
    "厨房,卫生间,阳台墙面防水",
    "保温隔热屋面 (屋面一倒置式上人保温平屋面)",
    "保温隔热屋面 (屋面二不上人保温屋面)",
    "保温隔热墙面（套内房间(客厅、卧室等外墙)、商铺外墙）",
    "保温柱、梁面",
    "外墙1 外墙面砖",
    "外墙2 外墙涂料",
    "内墙一 面砖墙面 （住宅入口门厅、电梯前室、走道、扩大前室）",
    "内墙二 涂料墙面 （楼梯间、住宅楼梯间、电梯机房）",
    "内墙二 墙面抹灰",
    "内墙三 墙面抹灰 （套内房间(客厅、卧室等内隔墙)、水井、电井、通风井、商铺内隔墙）",
    "内墙四 墙面抹灰 （卫生间、厨房、阳台）",
    "柱、梁面一般抹灰（水泥砂浆）",
    "柱、梁面一般抹灰（混合砂浆）",
    "地面二 水泥砂浆地面 （在地下室上部的商铺、强电井弱电井、配电间、弱电间、电梯井）",
    "地面三 水泥砂浆地面 （不在地下室上部的商铺卫生间）",
    "地面四 水泥砂浆地面（楼梯间）",
    "地面五 大理石地面 （住宅入口门厅,扩大前室）",
    "地面六 地砖地面（物管用房,消防控制室）",
    "楼面一 水泥砂浆楼面（厨房,卫生间,阳台）",
    "楼面二 地砖楼面（电梯厅,公共走道）",
    "楼面三 水泥砂浆楼面（主卧室、次卧室、客厅、餐厅、电梯机房、屋顶）",
    "顶棚2 涂料顶棚 （楼梯间）",
    "顶棚3 吊顶顶棚 （住宅入口门厅、电梯前室）",
    "矩形柱（含超高模板增加费）",
    "矩形梁（含超高模板增加费）",
    "直形墙（含超高模板增加费）",
    "空调板、飘窗板、雨棚板",
    "其它现浇构件",
    "卫生间翻边",
    "散水",
    "预制沟盖板",
    "垂直运输",
    "超高施工增加",
    "大型机械设备进出场及安拆 履带履带式挖掘机",
    "大型机械设备进出场及安拆 塔式起重机",
    "大型机械设备进出场及安拆 施工电梯",
    "大型机械设备进出场及安拆 旋挖钻机",
    "成井",
    '排水、降水'
     ]

for i in range(len(l)):
    print(chinese_to_pinyin(l[i]).replace(' ', '_').replace('，', '').replace('、', '').replace('（', '').replace('）', ''))  # 输出: 'ni3 hao3 shi4 jie4'

