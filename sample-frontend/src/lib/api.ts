import axios from 'axios';

// Interfaces for our data structures
export interface WeatherData {
  temperature: number;
  condition: string;
  // Add more weather properties as needed
}

export interface BusData {
  id: string;
  routeId: string;
  position: {
    latitude: number;
    longitude: number;
  };
  timestamp: string;
  vehicle: {
    id: string;
    label: string;
  };
  occupancyStatus?: string;
}

export interface TrainData {
  TRAIN_ID: string;
  LINE: string;
  STATION: string;
  DIRECTION: string;
  NEXT_ARR: string;
  WAITING_TIME: string;
  DELAY: string;
  LATITUDE: string;
  LONGITUDE: string;
  DESTINATION: string;
}

export interface TransitStatus {
  busStatus: {
    status: 'On Time' | 'Minor Delays' | 'Major Delays';
    percentage: number;
    details: string;
  };
  trainStatus: {
    status: 'On Time' | 'Minor Delays' | 'Major Delays';
    details: string;
    affectedLines: {
      line: string;
      delay: string;
    }[];
  };
}

// Base URL for API requests
const API_BASE_URL = 'http://localhost:5001/api';

// Weather API
export const getWeatherData = async (): Promise<WeatherData> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/weather`);
    return response.data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    // Return default data if API fails
    return {
      temperature: 72,
      condition: 'Partly Cloudy'
    };
  }
};

// Bus positions API
export const getBusPositions = async (): Promise<BusData[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/buses/positions`);
    // Extract the bus positions from the response
    return response.data.entity.map((entry: any) => entry.vehicle);
  } catch (error) {
    console.error('Error fetching bus positions:', error);
    return [];
  }
};

// Bus trip updates API
export const getBusTripUpdates = async (): Promise<any> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/buses/trips`);
    return response.data;
  } catch (error) {
    console.error('Error fetching bus trip updates:', error);
    return [];
  }
};

// Train data API
export const getTrainData = async (): Promise<TrainData[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/trains`);
    return response.data;
  } catch (error) {
    console.error('Error fetching train data:', error);
    return [];
  }
};

// Transit status API
export const getTransitStatus = async (): Promise<TransitStatus> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/status`);
    return response.data;
  } catch (error) {
    console.error('Error fetching transit status:', error);
    // Return default status if API fails
    return {
      busStatus: {
        status: 'On Time',
        percentage: 95,
        details: '95% of routes operating normally'
      },
      trainStatus: {
        status: 'Minor Delays',
        details: 'Red Line: 5-10 minute delays',
        affectedLines: [
          {
            line: 'RED',
            delay: '5-10 minutes'
          }
        ]
      }
    };
  }
};

// Recent updates API
export const getRecentUpdates = async (): Promise<{type: string, message: string}[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/updates`);
    return response.data;
  } catch (error) {
    console.error('Error fetching recent updates:', error);
    // Return default updates if API fails
    return [
      { type: 'on-time', message: 'Route 110 operating on schedule' },
      { type: 'delayed', message: 'Weather advisory: Expect delays on north-bound routes' },
      { type: 'disrupted', message: 'Service disruption on Blue Line between Stations A and B' }
    ];
  }
}; 