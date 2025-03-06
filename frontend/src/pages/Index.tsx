
import { useState } from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { CloudSun, Bus, TrainFront } from "lucide-react";
import { Button } from "@/components/ui/button";
import { LiveMap } from "@/components/LiveMap";

const Overview = () => {
  const [mapType, setMapType] = useState<"bus" | "train">("bus");

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <main className="flex-1 p-6">
          <SidebarTrigger />
          <div className="max-w-7xl mx-auto space-y-6">
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
              <div className="transit-card animate-in" style={{ animationDelay: "0.1s" }}>
                <div className="flex items-center gap-4 mb-4">
                  <div className="p-3 rounded-full bg-blue-50">
                    <CloudSun className="h-6 w-6 text-blue-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Weather</h3>
                    <p className="text-sm text-muted-foreground">Current Conditions</p>
                  </div>
                </div>
                <div className="text-2xl font-semibold">72°F</div>
                <p className="text-sm text-muted-foreground">Partly Cloudy</p>
              </div>

              <div className="transit-card animate-in" style={{ animationDelay: "0.2s" }}>
                <div className="flex items-center gap-4 mb-4">
                  <div className="p-3 rounded-full bg-green-50">
                    <Bus className="h-6 w-6 text-green-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Bus Status</h3>
                    <p className="text-sm text-muted-foreground">System-wide</p>
                  </div>
                </div>
                <div className="text-2xl font-semibold text-transit-on-time">
                  On Time
                </div>
                <p className="text-sm text-muted-foreground">
                  95% of routes operating normally
                </p>
              </div>

              <div className="transit-card animate-in" style={{ animationDelay: "0.3s" }}>
                <div className="flex items-center gap-4 mb-4">
                  <div className="p-3 rounded-full bg-purple-50">
                    <TrainFront className="h-6 w-6 text-purple-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Train Status</h3>
                    <p className="text-sm text-muted-foreground">All Lines</p>
                  </div>
                </div>
                <div className="text-2xl font-semibold text-transit-delayed">
                  Minor Delays
                </div>
                <p className="text-sm text-muted-foreground">
                  Red Line: 5-10 minute delays
                </p>
              </div>
            </div>

            {/* Live Map Section */}
            <div className="transit-card animate-in" style={{ animationDelay: "0.4s" }}>
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
              <div className="h-[600px]">
                <LiveMap type={mapType} />
              </div>
            </div>

            {/* Recent Updates */}
            <div className="transit-card animate-in" style={{ animationDelay: "0.7s" }}>
              <h2 className="text-xl font-semibold mb-4">Recent Updates</h2>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="h-2 w-2 rounded-full bg-transit-on-time" />
                  <p className="text-sm">
                    Route 110 operating on schedule
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="h-2 w-2 rounded-full bg-transit-delayed" />
                  <p className="text-sm">
                    Weather advisory: Expect delays on north-bound routes
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="h-2 w-2 rounded-full bg-transit-disrupted" />
                  <p className="text-sm">
                    Service disruption on Blue Line between Stations A and B
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Overview;
