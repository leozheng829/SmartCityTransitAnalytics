
import { useState } from "react";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Button } from "@/components/ui/button";
import { Bus, TrainFront } from "lucide-react";
import { LiveMap } from "@/components/LiveMap";

const MapPage = () => {
  const [mapType, setMapType] = useState<"bus" | "train">("bus");

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <main className="flex-1">
          <div className="p-6">
            <SidebarTrigger />
            <div className="mb-4 flex justify-between items-center">
              <h1 className="text-2xl font-bold">Live Transit Map</h1>
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
            <LiveMap type={mapType} />
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default MapPage;
