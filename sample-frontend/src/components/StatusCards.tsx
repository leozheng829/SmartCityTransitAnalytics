import React from 'react';
import { CloudSun, Bus, TrainFront, AlertTriangle } from 'lucide-react';
import { WeatherData, TransitStatus } from '@/lib/api';

interface StatusCardProps {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  value: string;
  detail: string;
  status?: 'on-time' | 'delayed' | 'disrupted';
  loading?: boolean;
  error?: string | null;
}

const StatusCard: React.FC<StatusCardProps> = ({
  icon,
  title,
  subtitle,
  value,
  detail,
  status,
  loading = false,
  error = null,
}) => {
  let statusColor = '';
  
  if (status === 'on-time') {
    statusColor = 'text-green-500';
  } else if (status === 'delayed') {
    statusColor = 'text-amber-500';
  } else if (status === 'disrupted') {
    statusColor = 'text-red-500';
  }
  
  return (
    <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      <div className="flex items-center gap-4 mb-4">
        {icon}
        <div>
          <h3 className="font-semibold">{title}</h3>
          <p className="text-sm text-muted-foreground">{subtitle}</p>
        </div>
      </div>
      
      {loading ? (
        <div className="text-2xl font-semibold text-muted-foreground">Loading...</div>
      ) : error ? (
        <div className="flex items-center gap-2 text-red-500">
          <AlertTriangle size={18} />
          <span>Unable to load data</span>
        </div>
      ) : (
        <>
          <div className={`text-2xl font-semibold ${statusColor}`}>{value}</div>
          <p className="text-sm text-muted-foreground">{detail}</p>
        </>
      )}
    </div>
  );
};

interface WeatherCardProps {
  weatherData: WeatherData | null;
  loading?: boolean;
  error?: string | null;
}

export const WeatherCard: React.FC<WeatherCardProps> = ({ 
  weatherData,
  loading = false,
  error = null,
}) => {
  return (
    <StatusCard
      icon={<div className="p-3 rounded-full bg-blue-50">
              <CloudSun className="h-6 w-6 text-blue-500" />
            </div>}
      title="Weather"
      subtitle="Current Conditions"
      value={weatherData ? `${weatherData.temperature}°F` : '--°F'}
      detail={weatherData ? weatherData.condition : 'Weather data unavailable'}
      loading={loading}
      error={error}
    />
  );
};

interface BusStatusCardProps {
  transitStatus: TransitStatus | null;
  loading?: boolean;
  error?: string | null;
}

export const BusStatusCard: React.FC<BusStatusCardProps> = ({
  transitStatus,
  loading = false,
  error = null,
}) => {
  let status: 'on-time' | 'delayed' | 'disrupted' = 'on-time';
  
  if (transitStatus?.busStatus) {
    if (transitStatus.busStatus.status === 'Minor Delays') {
      status = 'delayed';
    } else if (transitStatus.busStatus.status === 'Major Delays') {
      status = 'disrupted';
    }
  }
  
  return (
    <StatusCard
      icon={<div className="p-3 rounded-full bg-green-50">
              <Bus className="h-6 w-6 text-green-500" />
            </div>}
      title="Bus Status"
      subtitle="System-wide"
      value={transitStatus?.busStatus?.status || 'Unknown'}
      detail={transitStatus?.busStatus?.details || 'Status information unavailable'}
      status={status}
      loading={loading}
      error={error}
    />
  );
};

interface TrainStatusCardProps {
  transitStatus: TransitStatus | null;
  loading?: boolean;
  error?: string | null;
}

export const TrainStatusCard: React.FC<TrainStatusCardProps> = ({
  transitStatus,
  loading = false,
  error = null,
}) => {
  let status: 'on-time' | 'delayed' | 'disrupted' = 'on-time';
  
  if (transitStatus?.trainStatus) {
    if (transitStatus.trainStatus.status === 'Minor Delays') {
      status = 'delayed';
    } else if (transitStatus.trainStatus.status === 'Major Delays') {
      status = 'disrupted';
    }
  }
  
  return (
    <StatusCard
      icon={<div className="p-3 rounded-full bg-purple-50">
              <TrainFront className="h-6 w-6 text-purple-500" />
            </div>}
      title="Train Status"
      subtitle="All Lines"
      value={transitStatus?.trainStatus?.status || 'Unknown'}
      detail={transitStatus?.trainStatus?.details || 'Status information unavailable'}
      status={status}
      loading={loading}
      error={error}
    />
  );
}; 