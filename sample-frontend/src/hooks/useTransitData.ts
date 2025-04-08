import { useState, useEffect } from 'react';
import { getWeatherData, getBusPositions, getTrainData, getTransitStatus, getRecentUpdates, WeatherData, BusData, TrainData, TransitStatus } from '@/lib/api';

interface TransitDataState {
  weather: WeatherData | null;
  busPositions: BusData[];
  trainData: TrainData[];
  transitStatus: TransitStatus | null;
  recentUpdates: { type: string; message: string }[];
  loading: {
    weather: boolean;
    busPositions: boolean;
    trainData: boolean;
    transitStatus: boolean;
    recentUpdates: boolean;
  };
  error: {
    weather: string | null;
    busPositions: string | null;
    trainData: string | null;
    transitStatus: string | null;
    recentUpdates: string | null;
  };
}

export const useTransitData = () => {
  const [data, setData] = useState<TransitDataState>({
    weather: null,
    busPositions: [],
    trainData: [],
    transitStatus: null,
    recentUpdates: [],
    loading: {
      weather: true,
      busPositions: true,
      trainData: true,
      transitStatus: true,
      recentUpdates: true,
    },
    error: {
      weather: null,
      busPositions: null,
      trainData: null,
      transitStatus: null,
      recentUpdates: null,
    },
  });

  // Fetch weather data
  const fetchWeatherData = async () => {
    try {
      const weatherData = await getWeatherData();
      setData(prevData => ({
        ...prevData,
        weather: weatherData,
        loading: { ...prevData.loading, weather: false },
        error: { ...prevData.error, weather: null },
      }));
    } catch (error) {
      console.error('Error fetching weather data:', error);
      setData(prevData => ({
        ...prevData,
        loading: { ...prevData.loading, weather: false },
        error: { ...prevData.error, weather: 'Failed to load weather data' },
      }));
    }
  };

  // Fetch bus positions
  const fetchBusPositions = async () => {
    try {
      const busData = await getBusPositions();
      setData(prevData => ({
        ...prevData,
        busPositions: busData,
        loading: { ...prevData.loading, busPositions: false },
        error: { ...prevData.error, busPositions: null },
      }));
    } catch (error) {
      console.error('Error fetching bus positions:', error);
      setData(prevData => ({
        ...prevData,
        loading: { ...prevData.loading, busPositions: false },
        error: { ...prevData.error, busPositions: 'Failed to load bus data' },
      }));
    }
  };

  // Fetch train data
  const fetchTrainData = async () => {
    try {
      const trainData = await getTrainData();
      setData(prevData => ({
        ...prevData,
        trainData,
        loading: { ...prevData.loading, trainData: false },
        error: { ...prevData.error, trainData: null },
      }));
    } catch (error) {
      console.error('Error fetching train data:', error);
      setData(prevData => ({
        ...prevData,
        loading: { ...prevData.loading, trainData: false },
        error: { ...prevData.error, trainData: 'Failed to load train data' },
      }));
    }
  };

  // Fetch transit status
  const fetchTransitStatus = async () => {
    try {
      const statusData = await getTransitStatus();
      setData(prevData => ({
        ...prevData,
        transitStatus: statusData,
        loading: { ...prevData.loading, transitStatus: false },
        error: { ...prevData.error, transitStatus: null },
      }));
    } catch (error) {
      console.error('Error fetching transit status:', error);
      setData(prevData => ({
        ...prevData,
        loading: { ...prevData.loading, transitStatus: false },
        error: { ...prevData.error, transitStatus: 'Failed to load transit status' },
      }));
    }
  };

  // Fetch recent updates
  const fetchRecentUpdates = async () => {
    try {
      const updates = await getRecentUpdates();
      setData(prevData => ({
        ...prevData,
        recentUpdates: updates,
        loading: { ...prevData.loading, recentUpdates: false },
        error: { ...prevData.error, recentUpdates: null },
      }));
    } catch (error) {
      console.error('Error fetching recent updates:', error);
      setData(prevData => ({
        ...prevData,
        loading: { ...prevData.loading, recentUpdates: false },
        error: { ...prevData.error, recentUpdates: 'Failed to load recent updates' },
      }));
    }
  };

  // Refresh all data
  const refreshAllData = () => {
    setData(prevData => ({
      ...prevData,
      loading: {
        weather: true,
        busPositions: true,
        trainData: true,
        transitStatus: true,
        recentUpdates: true,
      },
    }));
    
    fetchWeatherData();
    fetchBusPositions();
    fetchTrainData();
    fetchTransitStatus();
    fetchRecentUpdates();
  };

  // Initial data fetch
  useEffect(() => {
    fetchWeatherData();
    fetchBusPositions();
    fetchTrainData();
    fetchTransitStatus();
    fetchRecentUpdates();

    // Set up refresh interval (every 30 seconds)
    const intervalId = setInterval(refreshAllData, 30000);

    // Clean up interval on unmount
    return () => clearInterval(intervalId);
  }, []);

  return {
    ...data,
    refreshAllData,
    refreshWeather: fetchWeatherData,
    refreshBusPositions: fetchBusPositions,
    refreshTrainData: fetchTrainData,
    refreshTransitStatus: fetchTransitStatus,
    refreshRecentUpdates: fetchRecentUpdates,
  };
}; 