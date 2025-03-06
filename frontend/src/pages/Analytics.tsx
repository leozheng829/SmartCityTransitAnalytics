
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { time: '00:00', passengers: 1000, delays: 2 },
  { time: '04:00', passengers: 500, delays: 1 },
  { time: '08:00', passengers: 4000, delays: 8 },
  { time: '12:00', passengers: 3000, delays: 5 },
  { time: '16:00', passengers: 5000, delays: 10 },
  { time: '20:00', passengers: 2000, delays: 4 },
];

const Analytics = () => {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <main className="flex-1 p-6">
          <SidebarTrigger />
          <div className="max-w-6xl mx-auto space-y-8">
            <header>
              <h1 className="text-2xl font-bold">Transit Analytics</h1>
              <p className="text-muted-foreground">System performance and statistics</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="transit-card">
                <h2 className="text-lg font-semibold mb-4">Passenger Flow</h2>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="passengers" stroke="#8884d8" fill="#8884d8" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="transit-card">
                <h2 className="text-lg font-semibold mb-4">Delay Incidents</h2>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="delays" stroke="#82ca9d" fill="#82ca9d" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Analytics;