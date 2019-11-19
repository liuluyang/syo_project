
import execjs


id = 'DcOOwrkRADEIBMOBwpQQLMKfwokEw6Qfw5LCnTlGVw3Dg8KEw7fDpsOdwrfDuyIsw5TCqcKfw799L0hjwpVaWcKnw6IQV8OwCcOwwpEBSSXCqUDDu8OSw4xEVGxww5jDgMOTw57DssKUesKhw6TCgsOFw6Btwo1qwoIWCURGw57Dmkl+w6jCk8KiScKiwppJw5TCrnQLw4/CsgXDoxjDlcOfZsKOD14vEMKDwoPDisK1WsKqaMKdw790QT5Zw48TbsKBwpvCsSskwrccw7gA'

with open('list.js', encoding='utf8') as f:
    file = f.read()
    ctx = execjs.compile(file)
    r = ctx.call('Navi', id, '')
    print(r)