# Pulse-Sensor

心拍センサの使い方、使うためのセットアップ等を記述する。

# Hardware

* Raspberry Pi Zero WH

* PulseSensor

* MCP3008(A/Dコンバータ)

# Cirsuit Diagram

ラズパイ→MCP3008

3.3V → Vref, Vdd

GND　→ AGND, DGND

8(SPIO-CE0) → CS/SHDN

10(SPIO-MOSI) → Din

9(SPIO-MISO) → Dout

11(SPIO-SCLK) → CLK

のようにつないで、MCP3008のCH0から心拍センサを通す。

* [Raspberry Pi zeroのピン配置](http://hara.jpn.com/_default/ja/Topics/RaspPiZero.html)

* [MCP3008のピン配置](http://ww1.microchip.com/downloads/en/DeviceDoc/21295d.pdf)

* [回路図](https://tutorials-raspberrypi.com/wp-content/uploads/Raspberry-Pi-MCP3008-ADC-Anschluss-Steckplatine.png)

# Requirement

* python 3.7.3
* spidev 3.4

# Installation

(1)GUIの設定メニューからSPIを有効にして再起動。
→設定→Raspberry Piの設定→インターフェース

(2)SPIが有効になったか確認。
→spi-bcm2835とか出てくればOK。

```bash
lsmod | grep spi
```

(3)pi-spidevライブラリのインストール

```bash
sudo apt-get install python-pip
sudo pip3 install spidev
```

# Usage

* pulse-wave:値を0.01秒ごとに計測してcsc形式で保存

* pulse-peak:心拍のピークを検出してprint

# Note

質問あればslack投げて。

親指、人差し指、耳たぶでデータを取ったが閾値530は妥当だった。

# Author

* Fumihito Oki
