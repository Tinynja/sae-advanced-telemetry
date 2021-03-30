#ifndef SPORT_H
	#define SPORT_H

	#define SPORT_BAUD 57600
	#define SPORT_POLL 0x7E
	#define SPORT_ALL_HUBIDS 0xFF
	#define SPORT_HEADER_DISCARD 0x00
	#define SPORT_HEADER_DATA 0x10
	#define SPORT_HEADER_READ 0x30
	#define SPORT_HEADER_WRITE 0x31
	#define SPORT_HEADER_RESPONSE 0x32

	#include <Arduino.h>

	#include <DataTypes.h>
	#include <SPortStandardSensorIDs.h>
	#include <SPortSensor.h>

	#include <SPortHub.h>

#endif