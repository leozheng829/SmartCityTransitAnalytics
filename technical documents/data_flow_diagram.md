# MARTA Transit Dashboard - Data Flow Diagram

## Overview

This document describes the flow of data through the MARTA Transit Dashboard system using text-based diagrams. While a full graphical diagram would be ideal, this text representation captures the essential data flows.

## High-Level Data Flow

```
                 ┌───────────────────┐
                 │                   │
┌─────────────┐  │  MARTA            │  ┌─────────────┐
│             │  │  Transit APIs     │  │             │
│ Weather API ├──┤  - Train API      ├──┤ User Browser│
│             │  │  - Bus GTFS-RT    │  │             │
└─────────────┘  │                   │  └──────┬──────┘
                 └───────────────────┘         │
                          ▲                    │
                          │                    │
                 ┌────────┴────────┐           │
                 │                 │           │
                 │ Flask           │◄──────────┘
                 │ Application     │
                 │                 │
                 └────────┬────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │                │
                 │ Cache System   │
                 │                │
                 └────────────────┘
```

## Detailed Data Flow

### 1. External Data Acquisition

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  MARTA          │      │  MARTA GTFS-RT  │      │  Weather API    │
│  Train API      │      │  Bus API        │      │                 │
│                 │      │                 │      │                 │
└────────┬────────┘      └────────┬────────┘      └────────┬────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│                │      │                │      │                │
│ train_data.py  │      │  bus_data.py   │      │  weather.py    │
│                │      │                │      │                │
└────────┬───────┘      └────────┬───────┘      └────────┬───────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                       ┌────────────────┐
                       │                │
                       │  Cache System  │
                       │                │
                       └────────┬───────┘
                                │
                                ▼
                       ┌────────────────┐
                       │                │
                       │  API Routes    │
                       │                │
                       └────────────────┘
```

### 2. Client Data Request Flow

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  Browser        │─┐    │  Web Routes     │─┐    │  API Routes     │
│  (index.html)   │ │    │  (routes.py)    │ │    │  (api/routes.py)│
│                 │ │    │                 │ │    │                 │
└─────────────────┘ │    └─────────────────┘ │    └────────┬────────┘
                    │                        │             │
                    │                        │             │
                    │    ┌─────────────────┐ │             │
                    └───►│                 │◄┘             │
                         │  Templates      │               │
                         │  (index.html)   │               │
                         │                 │               │
                         └─────────────────┘               │
                                                           │
                                                           ▼
                                                  ┌────────────────┐
                                                  │                │
                                                  │ Data Services  │
                                                  │                │
                                                  └────────┬───────┘
                                                           │
                                                           │
                                                           ▼
                                                  ┌────────────────┐
                                                  │                │
                                                  │ Cache System   │
                                                  │                │
                                                  └────────────────┘
```

### 3. Real-time Updates Flow

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  JavaScript     │      │  Fetch API      │      │  API Routes     │
│  (Client-side)  ├─────►│  AJAX Requests  ├─────►│  /api/trains    │
│                 │      │                 │      │  /api/buses     │
└─────────────────┘      └─────────────────┘      │  /api/weather   │
       ▲                                          │                 │
       │                                          └────────┬────────┘
       │                                                   │
       │                                                   │
       │                                           ┌───────▼────────-┐
       │                                           │                 │
       │                                           │  Data Services  │
       │                                           │                 │
       │                                           └────────┬────────┘
       │                                                    │
       │                                                    │
┌──────┴────────┐                                  ┌────────▼────────┐
│               │                                  │                 │
│ DOM Updates   │◄─────────────────────────────────┤ JSON Responses  │
│               │                                  │                 │
└───────────────┘                                  └─────────────────┘
```

## Map Data Flow

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│ Train Data     │     │ Bus Position   │     │ OpenStreetMap  │
│ API Response   │     │ API Response   │     │ Tile Server    │
│                │     │                │     │                │
└───────┬────────┘     └───────┬────────┘     └───────┬────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                        Leaflet.js                              │
│                                                                │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                  Interactive Map Display                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Station Filtering Flow

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│                │     │                │     │                │
│  User Click    │     │ Filter Logic   │     │ Train Data     │
│  on Station    ├────►│ by Station     ├────►│ Array          │
│                │     │                │     │                │
└────────────────┘     └────────────────┘     └───────┬────────┘
                                                      │
                                                      │
                                              ┌───────▼────────┐
                                              │                │
                                              │ Filtered       │
                                              │ Display Cards  │
                                              │                │
                                              └────────────────┘
```

## Notes

1. The actual data flow includes additional error handling and fallback paths not shown in these diagrams
2. The caching system serves as both a performance optimization and a reliability mechanism
3. All external API calls include retry logic and error handling