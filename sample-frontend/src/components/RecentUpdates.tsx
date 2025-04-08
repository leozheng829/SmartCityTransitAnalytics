import React from 'react';
import { AlertTriangle, Clock, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface RecentUpdatesProps {
  updates: { type: string; message: string }[];
  loading?: boolean;
  error?: string | null;
  onRefresh?: () => void;
}

export const RecentUpdates: React.FC<RecentUpdatesProps> = ({
  updates,
  loading = false,
  error = null,
  onRefresh,
}) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Recent Updates</h2>
        {onRefresh && (
          <Button variant="ghost" size="sm" onClick={onRefresh} disabled={loading}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        )}
      </div>
      
      {loading ? (
        <div className="flex items-center justify-center p-4 text-muted-foreground">
          <Clock className="animate-spin h-5 w-5 mr-2" />
          <span>Loading updates...</span>
        </div>
      ) : error ? (
        <div className="flex items-center justify-center p-4 text-red-500">
          <AlertTriangle className="h-5 w-5 mr-2" />
          <span>{error}</span>
        </div>
      ) : updates.length === 0 ? (
        <div className="p-4 text-center text-muted-foreground">
          No recent updates available
        </div>
      ) : (
        <div className="space-y-4">
          {updates.map((update, index) => {
            let dotColor = 'bg-green-500';
            if (update.type === 'delayed') {
              dotColor = 'bg-amber-500';
            } else if (update.type === 'disrupted') {
              dotColor = 'bg-red-500';
            }
            
            return (
              <div key={index} className="flex items-center gap-4">
                <div className={`h-2 w-2 rounded-full ${dotColor}`} />
                <p className="text-sm">{update.message}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}; 