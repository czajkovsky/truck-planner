# Truck Planner

This repository solves CVRP (capacitated vehicle routing problem).

## World description
Our task is to manage imaginated factory. We own one data center and fleet that includes multiple types of vehicles. Our product is quite popular and we are suppling around 100 cities. The demand changes on daily basis and it needs to be covered in 100%.

## Prerequisites
To run this code you will need:
* [Python](https://www.python.org/downloads/) (tested on v2.7.6)
* [Gurobi Optimizer](http://user.gurobi.com/download/gurobi-optimizer) (tested on v6.5.0, academic license)
* [PIP](https://pip.pypa.io/en/stable/) (tested on v7.1.2)

## Installing
```
pip install tabulate
```

## Running
```
python batch.py
```

## Configuration
Inside batch.py you can find some configuration variables:
* `SIMPLE_MODE` - max delivery points and max daily distance is not taken into account
* `BATCHES_SIZE`

## Input
You can find two datasets in [data](https://github.com/czajkovsky/vrp/tree/master/data). Each dataset should be stored in sepearte folder and include following files:
* `distances.csv` - distances between cities
* `fleet.csv` - available fleet description
* `orders*.csv` - list of demands

You can change the dataset with `Importer` class. For example:
```py
# parameters
# - module name (string)
# - orders suffix (string)
# - data center key (string
# - run in simple mode (bool)
# - batches size (int)

importer = Importer('demo', '-2013-02-01', 'DC', True, 10)
```
Will look for
* `data/demo/distances.csv`
* `data/demo/fleet.csv`
* `data/demo/orders-2013-02-01.csv`

### Files structure

Each of the `.csv` file should be `;` seperated and include header row.

#### Distances
| From   | To     | Distance |
| ------ | ------ | -------- |
| Poznan | Warsaw | 301      |
| Warsaw | Poznan | 310      |
Please note that from `i` to `j` can be different than `j` to `i`.

#### Fleet
| Type    | Count | Capacity | Price per 1km | Max Daily Distance | Max delivery points |
| ------- | ----- | -------- | ------------- | ------------------ | ------------------- |
| TIR     | 2     | 33       | 1.89          | 1000               | 3                   |
| Transit | 5     | 10       | 1.02          | 500                | 10                  |

#### Orders
| City   | Demand |
| ------ | ------ |
| Poznan | 56     |
| Warsaw | 2      |

## Output
As the result code returns plan for all trucks. You can see an example below:
```
  BATCH  DIST             COST  TRUCK           PALETTES  ROUTE
-------  ----------  ---------  ------------  ----------  ----------------------------------------------------
      1  319.97 km    534.35    TYP_100CF_01           9  FACTORY -> TORUN_1 -> FACTORY
      1  332.88 km    672.418   TYP_160CF             17  FACTORY -> TORUN_3 -> TORUN_2 -> FACTORY
      1  688.88 km   1150.43    TYP_100CF_02          12  FACTORY -> KIELCE -> FACTORY
      1  609.95 km   1329.69    TYP_190CF             18  FACTORY -> WARSZAWA_STAWKI -> FACTORY
      2  432.54 km    722.342   TYP_100CF_02           7  FACTORY -> GRUDZIADZ_1 -> FACTORY
      2  446.21 km    972.738   TYP_190CF             19  FACTORY -> GRUDZIADZ_2 -> FACTORY
      2  993.49 km   1738.61    TYP_120CF             13  FACTORY -> BIALYSTOK_1 -> BIALYSTOK_2 -> FACTORY
      2  140.59 km    246.032   TYP_120CF             15  FACTORY -> PNIEWY -> FACTORY
      3  598.94 km   1000.23    TYP_100CF_01          10  FACTORY -> GDANSK_4 -> FACTORY
      3  236.53 km    395.005   TYP_100CF_01          10  FACTORY -> INOWROCLAW -> FACTORY
      3  305.87 km    510.803   TYP_100CF_02           9  FACTORY -> LUBIN -> GLOGOW_2 -> GLOGOW_1 -> FACTORY
      4  45.38 km      98.9284  TYP_190CF             18  FACTORY -> POZNAN_T -> FACTORY
      4  40.15 km      87.527   TYP_190CF             18  FACTORY -> POZNAN_PLA -> FACTORY
      4  814.99 km   1361.03    TYP_100CF_02          10  FACTORY -> BIELSKO_BIALA -> FACTORY
      4  622.41 km   1587.15    TYP_TR+SEMCF          32  FACTORY -> WARSZAWA_TARCH -> FACTORY
      4  604.17 km   1057.3     TYP_120CF             13  FACTORY -> WARSZAWA_BL#0 -> FACTORY
      5  321.67 km    562.922   TYP_120CF             14  FACTORY -> ZIELONA_GORA_2 -> FACTORY
      5  284.21 km    289.894   TYP_035CF              2  FACTORY -> ZLOTOW -> FACTORY
      5  604.97 km   1318.83    TYP_190CF             18  FACTORY -> WARSZAWA_J -> FACTORY
      5  201.69 km    407.414   TYP_160CF             16  FACTORY -> LESZNO_2 -> JAROCIN -> FACTORY
      6  156.41 km    261.205   TYP_100CF_02           8  FACTORY -> LESZNO_1 -> FACTORY
      6  622.74 km    635.195   TYP_035CF              4  FACTORY -> JOZEFOSLAW -> FACTORY
      6  42.25 km      73.9375  TYP_120CF             15  FACTORY -> POZNAN_PLE -> FACTORY
      6  28.73 km      47.9791  TYP_100CF_02          12  FACTORY -> SWARZEDZ -> FACTORY
      6  234.6 km     239.292   TYP_035CF              4  FACTORY -> PILA_2 -> FACTORY
      7  28.72 km      73.236   TYP_TR+SEMCF          26  FACTORY -> LUBON -> FACTORY
      7  28.36 km      57.2872  TYP_160CF             17  FACTORY -> POZNAN_B -> FACTORY
      7  650.62 km   1659.08    TYP_TR+SEMCF          26  FACTORY -> GDANSK_3 -> GDANSK_2 -> PILA_1 -> FACTORY
      8  625.74 km   1364.11    TYP_190CF             19  FACTORY -> GDANSK_1 -> TCZEW -> FACTORY
      8  34.55 km      88.1025  TYP_TR+SEMCF          24  FACTORY -> POZNAN_H -> FACTORY
      8  705.22 km   1234.13    TYP_120CF             14  FACTORY -> KATOWICE -> FACTORY
      8  27.59 km      55.7318  TYP_160CF             16  FACTORY -> POZNAN_R -> FACTORY
      9  22.06 km      36.8402  TYP_100CF_01          10  FACTORY -> POZNAN_Z -> FACTORY
      9  571.35 km    582.777   TYP_035CF              3  FACTORY -> BRWINOW -> FACTORY
      9  309.2 km     516.364   TYP_100CF_02          10  FACTORY -> WROCLAW_5 -> FACTORY
      9  35.8 km       62.65    TYP_120CF             13  FACTORY -> POZNAN_GR -> FACTORY
      9  307.6 km     538.3     TYP_120CF             15  FACTORY -> WROCLAW_3 -> FACTORY
     10  312.97 km    522.66    TYP_100CF_02          12  FACTORY -> WROCLAW_2 -> FACTORY
     10  311.65 km    545.387   TYP_120CF             13  FACTORY -> WROCLAW_1 -> FACTORY
     10  40.32 km      70.56    TYP_120CF             14  FACTORY -> POZNAN_MAR -> FACTORY
     10  768.69 km    784.064   TYP_035CF              4  FACTORY -> CHRZANOW -> FACTORY
     10  27.18 km      69.309   TYP_TR+SEMCF          22  FACTORY -> POZNAN_MAL -> FACTORY
     11  341.6 km     597.8     TYP_120CF             15  FACTORY -> GORZOW_1 -> FACTORY
     11  263.38 km    460.915   TYP_120CF             13  FACTORY -> POZNAN_GL -> DREZDENKO -> FACTORY
     11  336.16 km    588.28    TYP_120CF             14  FACTORY -> GORZOW_2 -> FACTORY
     11  276.44 km    602.639   TYP_190CF             18  FACTORY -> BYDGOSZCZ_1 -> FACTORY
     12  281.17 km    612.951   TYP_190CF             18  FACTORY -> BYDGOSZCZ_3 -> FACTORY
     12  297.29 km    600.526   TYP_160CF             16  FACTORY -> BYDGOSZCZ_2 -> FACTORY
     12  320.79 km    327.206   TYP_035CF              6  FACTORY -> STRZELCE_KRAJENSKIE -> FACTORY
     12  1028.25 km  1717.18    TYP_100CF_01          11  FACTORY -> RZESZOW_1 -> FACTORY
     12  1043.83 km  1743.2     TYP_100CF_02          11  FACTORY -> RZESZOW_2 -> FACTORY
     12  313.33 km    523.261   TYP_100CF_02          12  FACTORY -> WROCLAW_4 -> FACTORY
     13  204.55 km    341.599   TYP_100CF_01          10  FACTORY -> TRZCIANKA -> FACTORY
     13  92.86 km     155.076   TYP_100CF_01          11  FACTORY -> OBORNIKI_WLKP -> FACTORY
     13  42.34 km      74.095   TYP_120CF             13  FACTORY -> SRODA_WLKP -> FACTORY
     13  331.89 km    338.528   TYP_035CF              3  FACTORY -> LEGNICA -> FACTORY
     13  47.92 km      80.0264  TYP_100CF_02          12  FACTORY -> SUCHY_LAS -> FACTORY
     13  546.23 km    912.204   TYP_100CF_02          11  FACTORY -> SZCZECIN_2 -> FACTORY
     14  561.14 km   1346.74    TYP_260CF             20  FACTORY -> SZCZECIN_1 -> SZCZECIN_3 -> FACTORY
     14  358.53 km    365.701   TYP_035CF              5  FACTORY -> SLUBICE -> FACTORY
     14  674.04 km   1469.41    TYP_190CF             19  FACTORY -> OLSZTYN -> FACTORY
     14  210.39 km    214.598   TYP_035CF              5  FACTORY -> KALISZ_1 -> FACTORY
     14  39.31 km     100.24    TYP_TR+SEMCF          22  FACTORY -> POZNAN_PRO -> FACTORY
     15  445.71 km   1136.56    TYP_TR+SEMCF          32  FACTORY -> PLOCK_1 -> PLOCK_2 -> PLOCK_3 -> FACTORY
     15  511.92 km   1228.61    TYP_260CF             20  FACTORY -> STARGARD_SZCZECINSKI -> FACTORY
     15  604.17 km   1540.63    TYP_TR+SEMCF          33  FACTORY -> WARSZAWA_BL#1 -> FACTORY
     15  604.17 km   1540.63    TYP_TR+SEMCF          33  FACTORY -> WARSZAWA_BL#2 -> FACTORY


===========
* Total cost:
    44180.4452
* Palettes delivered:
    964
FINISHED after 95.01s (BATCH SIZE: 5)
```

## Data manipulation
Before starting any computations data is processed:

1. Demands are filtered and cities without an order are completely removed and not included in computations. It's possible because each city is connected with another one.
2. Demands are divided into batches. Each batch consists of maximum `BATCHES_SIZE + 1` cities (demands).
3. Cities with demand higher than largest truck are divided into abstract, smaller ones. For example for:

  ```
  // bigest truck capacity = 33
  WARSAW;100
  ```
  is transformed to:
  ```
  WARSAW#0;1  // 100 % max capacity
  WARSAW#1;33 // max capacity
  WARSAW#2;33
  WARSAW#3;33
  ```

4. Fleet is equaly assigned to each batch (`count` / `batches`).

## Model logic

### Decision variables
There three decision variables:
* `x[i, j]` (type: `GRB.BINARY`) - route (`i` -> `j`) is used
* `t[i, j, ti]` (type: `GRB.BINARY`) - truck `ti` is used on route (`i` -> `j`)
* `u[i]` (type: `GRB.INTEGER`) - palettes for client `i`

### Objective
Our goal is to minimize transporation costs
```py
obj = quicksum(
  self.distances[i][j] * self.x[i,j] * self.t[i, j, ti] * self.trucks['rates'][ti]
  for i in sites
  for j in sites
  for ti in trucksRg
  if i != j
)
```

### Constraints
All constraints are defined in [world.py](https://github.com/czajkovsky/vrp/blob/master/logic/world.py).

1. There is only one incoming and one outgoing route per client.
2. Each existing connection has truck assigned.
3. Palettes in truck don't exceed truck capacity.
4. Incomming truck equals outgoing truck.
5. Don't exceed truck type count (if in simple mode).
6. Each truck (vehicle) can leave factory only once (if in advanced mode).
7. Don't exceed maximum daily distance and maxiumum delivery points (if in advanced mode).

### Results
Code was tested on MacBook Pro (13' Mid 2014; 2,8 GHz Intel Core i5; 16GB RAM). It was tested for multiple batch size for world instance which consists of
* **130** demands (**964** palettes)
* **8742** routes between **93** cities
* **152** trucks of **8** types

| Batch size | Result     | Duration | Batches count |
| ---------- | ---------- | -------- | ------------- |
| 5          | 44180.4452 | 95.01s   | 15            |
| 6          | 43376.5586 | 169.97s  | 13            |
| 7          | 43324.3908 | 1071.52s | 11            |
