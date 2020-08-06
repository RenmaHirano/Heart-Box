# Pulse-Sensor

圧力センサの使い方、使うためのセットアップ等を記述する。

# Hardware

* Raspberry Pi Zero WH

* FSR406(圧力センサ)

* 10kΩ抵抗

* MCP3002(A/Dコンバータ)

# Cirsuit Diagram

## ラズパイ→MCP3008

3.3V → Vdd/Vref(8)

GND　→ Vss(4)

8(SPIO-CE0) → CS/SHDN(1)

10(SPIO-MOSI) → Din(5)

9(SPIO-MISO) → Dout(6)

11(SPIO-SCLK) → CLK(7)

## その他
感圧センサを3.3VとMCP3002のCH0に繋ぐ。

CH0とGNDに10kΩ抵抗をさす。

* [Raspberry Pi zeroのピン配置](http://hara.jpn.com/_default/ja/Topics/RaspPiZero.html)

* [MCP3002のピン配置](http://akizukidenshi.com/download/ds/microchip/mcp3002.pdf)

* [回路図](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F88598%2Fcd32b7f7-cec5-10c2-9c91-25abec55a5c1.png?ixlib=rb-1.2.2&auto=format&gif-q=60&q=75&s=9da1be3ed30598e6215b0fff0f9e09ba)

# Requirement

* python 3.7.3
* spidev 3.4

# Installation

## py-spidev
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

* pressure:2つの感圧センサの0-1023の圧力値を出力

# Note

質問あればslack投げて。

# Author

* Fumihito Oki

