![Imagination Technologies Limited logo](../images/img.png)

# Creator System Test Framework

## Mikro-E 6LoWPAN Clicker <--> Ci40 Programming and serial port connection diagram

```
Ci40 Raspberry Pi interface                             Mikro-E 6LoWPAN Clicker
(40 pin Plug)                                           PicKit ICSP Interface

        /-----\                                                 /---\
    PGC |40 -------\      /-------------------------------------- 1 | RST
    PGD |38 -------|--\   |                     /---------------- 2 | 3V3
    RST |36 -------|--|---/   /-----------------|---------------- 3 | GND
    GND |34 ----\  |  \-------|-----------------|---------------- 4 | PGD
        |     | |  \----------|-----------------|---------------- 5 | PGC
        |  .  | \-------------/                 |             X-| 6 | NC
        |  .  |                                 |               \---/
        |  .  |                                 |                6-way 1.25mm pitch SIP connector
        |     |                                 |
UART2RX |10 -------------\                      |
UART2TX |8  -------------|---\                  |
        |6   5|          |   |                  |
        |4   3|          |   |                  |        Mikro-E 6LoWPAN clicker
        |2   1| 3V3 ----------------------------/          MikroBUS Connector
        \-----/          |   |                                  /---\
             .           |   |                                X-| 1 | NC
                         |   |                                X-| 2 | NC
                         |   \----------------------------------- 3 | UART2TX
                         \--------------------------------------- 4 | UART2RX
                                                              X-| 5 | NC
                                                              X-| 6 | NC
                                                              X-| 7 | NC
                                                              X-| 8 | NC
                                                                \---/
                                                                 8-way 1.25mm pitch SIP connector


-----------------------------------------------------------------------------------------------------------------------
|           |    Raspberry Pi connector              6LowPan clicker                                                  |
|           |                                        PicKit3 ICSPInterfacer Pin               MikroBUS connector pin  |
-----------------------------------------------------------------------------------------------------------------------
| PGC       |              40                                   5                                                     |
| PGD       |              38                                   4                                                     |
| RST       |              36                                   1                                                     |
| GND       |              34                                   3                                                     |
| UARTRX    |              10                                                                            4            |
| UARTTX    |               8                                                                            3            |
| 3V3       |               1                                   2                                                     |
-----------------------------------------------------------------------------------------------------------------------
```
