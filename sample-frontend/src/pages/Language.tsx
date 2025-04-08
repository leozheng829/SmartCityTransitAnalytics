
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const languages = [
  { code: "en", name: "English", active: true },
  { code: "es", name: "Español", active: false },
];

const Language = () => {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <main className="flex-1 p-6">
          <SidebarTrigger />
          <div className="max-w-xl mx-auto space-y-8">
            <header>
              <h1 className="text-2xl font-bold">Language Settings</h1>
              <p className="text-muted-foreground">Choose your preferred language</p>
            </header>

            <div className="transit-card">
              <div className="space-y-4">
                {languages.map((lang) => (
                  <Button
                    key={lang.code}
                    variant={lang.active ? "default" : "outline"}
                    className="w-full justify-between"
                  >
                    <span>{lang.name}</span>
                    {lang.active && <Check className="h-4 w-4" />}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Language;
