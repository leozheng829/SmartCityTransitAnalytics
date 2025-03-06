import React from 'react';

interface LiveMapProps {
  type: "bus" | "train";
}

export const LiveMap: React.FC<LiveMapProps> = ({ type }) => {
  return (
    <div className="w-full h-full rounded-lg overflow-hidden bg-gray-100 relative flex items-center justify-center">
      <div className="absolute inset-0 grid place-items-center">
        <div className="space-y-4 text-center">
          <div className={`text-4xl ${type === 'bus' ? 'text-green-500' : 'text-purple-500'}`}>
            {type === 'bus' ? '🚌' : '🚂'}
          </div>
          <div className="text-muted-foreground">
            {type === 'bus' ? 'Bus Routes Map' : 'Train Lines Map'}
          </div>
          <div className="text-sm text-muted-foreground">
            Live map integration coming soon
          </div>
        </div>
      </div>
      <div className="absolute inset-0">
        <div className="w-full h-full grid grid-cols-8 grid-rows-6">
          {Array.from({ length: 48 }).map((_, i) => (
            <div key={i} className="border border-gray-200"></div>
          ))}
        </div>
      </div>
    </div>
  );
};
