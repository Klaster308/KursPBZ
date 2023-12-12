CREATE DATABASE `kursovaya1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
use kursovaya1;
CREATE TABLE `dostavka` (
  `Id` int NOT NULL,
  `VremyaDostavki` timestamp NULL DEFAULT NULL,
  `Nomertelefona` varchar(255) DEFAULT NULL,
  `TipDostavki` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `klient` (
  `Id` int NOT NULL,
  `FIOZakazchika` varchar(255) DEFAULT NULL,
  `Nomertelefona` varchar(255) DEFAULT NULL,
  `Adres` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `mebel` (
  `Id` int NOT NULL,
  `Gabariti` varchar(255) DEFAULT NULL,
  `Color` varchar(255) DEFAULT NULL,
  `Materialy` varchar(255) DEFAULT NULL,
  `Ves` float DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `prodavec` (
  `Id` int NOT NULL,
  `FIOProdavca` varchar(255) DEFAULT NULL,
  `Nomertelefona` varchar(255) DEFAULT NULL,
  `Adres` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `zakaz` (
  `Id` int NOT NULL,
  `VremyaZakaza` timestamp NULL DEFAULT NULL,
  `GabaritiMebeli` varchar(255) DEFAULT NULL,
  `Material` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
