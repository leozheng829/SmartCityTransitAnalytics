import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Bus, TrainFront, RefreshCw } from "lucide-react";
import { LiveMap } from "@/components/LiveMap";
import { WeatherCard, BusStatusCard, TrainStatusCard } from "@/components/StatusCards";
import { RecentUpdates } from "@/components/RecentUpdates";
import { useTransitData } from "@/hooks/useTransitData";

const Overview = () => {
  const [mapType, setMapType] = useState<"bus" | "train">("bus");
  const {
    weather,
    transitStatus,
    recentUpdates,
    loading,
    error,
    refreshAllData,
    refreshRecentUpdates
  } = useTransitData();

  console.log("Rendering Overview component with data:", {
    weather,
    transitStatus,
    recentUpdates,
    loading,
    error
  });

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 relative">
      {/* Fixed Refresh Button */}
      <div className="fixed top-4 right-4 z-10">
        <Button 
          onClick={() => {
            console.log("Refresh button clicked");
            refreshAllData();
          }}
          disabled={Object.values(loading).some(status => status)}
          className="shadow-md"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh All Data
        </Button>
      </div>

      <div className="max-w-7xl mx-auto space-y-6 pt-10">
        <header className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            Smart City Transit Analytics
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Real-time transit information with integrated weather data for
            smarter urban mobility.
          </p>
        </header>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <WeatherCard 
            weatherData={weather} 
            loading={loading.weather}
            error={error.weather}
          />
          
          <BusStatusCard 
            transitStatus={transitStatus} 
            loading={loading.transitStatus}
            error={error.transitStatus}
          />
          
          <TrainStatusCard 
            transitStatus={transitStatus} 
            loading={loading.transitStatus}
            error={error.transitStatus}
          />
        </div>

        {/* Live Map Section */}
        <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
          <div className="mb-4 flex justify-between items-center">
            <h2 className="text-xl font-semibold">Live Transit Map</h2>
            <div className="flex gap-2">
              <Button
                variant={mapType === "bus" ? "default" : "outline"}
                onClick={() => setMapType("bus")}
              >
                <Bus className="mr-2 h-4 w-4" />
                Bus Map
              </Button>
              <Button
                variant={mapType === "train" ? "default" : "outline"}
                onClick={() => setMapType("train")}
              >
                <TrainFront className="mr-2 h-4 w-4" />
                Train Map
              </Button>
            </div>
          </div>
          <div className="h-[400px] md:h-[600px]">
            <LiveMap type={mapType} />
          </div>
        </div>

        {/* Recent Updates */}
        <RecentUpdates 
          updates={recentUpdates} 
          loading={loading.recentUpdates}
          error={error.recentUpdates}
          onRefresh={refreshRecentUpdates}
        />
      </div>
    </div>
  );
};

export default Overview;
