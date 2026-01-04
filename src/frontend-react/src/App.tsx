import { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { MapComponent } from '@/components/MapComponent';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { api, OptimizationRequest, Stop } from '@/api';
import { Loader2, Truck, Activity, Map as MapIcon, Clock } from 'lucide-react';
import { toast } from "sonner"
import { Toaster } from "@/components/ui/sonner"

// Default Data
const defaultInput = {
  "depot": {
    "lat": -34.6037,
    "lng": -58.3816,
    "address": "Obelisco (Depot)"
  },
  "stops": [
    {
      "lat": -34.6083,
      "lng": -58.3712,
      "address": "Casa Rosada"
    },
    {
      "lat": -34.6010,
      "lng": -58.3831,
      "address": "Teatro Colón"
    },
    {
      "lat": -34.6086,
      "lng": -58.3636,
      "address": "Puente de la Mujer (Pto Madero)"
    },
    {
      "lat": -34.6394,
      "lng": -58.3629,
      "address": "Caminito (La Boca)"
    },
    {
      "lat": -34.6212,
      "lng": -58.3732,
      "address": "Plaza Dorrego (San Telmo)"
    },
    {
      "lat": -34.5885,
      "lng": -58.3937,
      "address": "Cementerio de la Recoleta"
    },
    {
      "lat": -34.5697,
      "lng": -58.4116,
      "address": "Planetario (Palermo)"
    },
    {
      "lat": -34.5627,
      "lng": -58.4564,
      "address": "Barrio Chino (Belgrano)"
    },
    {
      "lat": -34.5513,
      "lng": -58.4513,
      "address": "Estadio Monumental (Núñez)"
    }
  ]
};

function App() {
  const [jsonInput, setJsonInput] = useState(JSON.stringify(defaultInput, null, 2));
  const [taskId, setTaskId] = useState<string | null>(null);
  const [stops, setStops] = useState<Stop[]>([]);
  const [optimizedOrder, setOptimizedOrder] = useState<string[]>([]);
  const [optimizationMetrics, setOptimizationMetrics] = useState<any>(null);

  // Parse stops for the map initially
  useEffect(() => {
    try {
      const parsed = JSON.parse(jsonInput);
      let mapStops: Stop[] = [];
      if (parsed.depot) {
        mapStops.push(parsed.depot);
      }
      if (parsed.stops) {
        mapStops = [...mapStops, ...parsed.stops];
      }
      setStops(mapStops);
    } catch (e) {
      // Invalid JSON, ignore for map update
    }
  }, [jsonInput]);

  // Mutation to Start Optimization
  const optimizeMutation = useMutation({
    mutationFn: (data: OptimizationRequest) => api.optimize(data),
    onSuccess: (data) => {
      setTaskId(data.task_id);
      setOptimizedOrder([]); // Reset previous result
      setOptimizationMetrics(null);
    },
    onError: (error) => {
      toast.error("Error starting optimization: " + error);
    }
  });

  // Query to Poll Status
  const { data: taskStatus } = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => api.getTaskStatus(taskId!),
    enabled: !!taskId && !optimizationMetrics, // Only poll if we have a Task ID and no result yet
    refetchInterval: (query) => {
      if (query.state.data?.status === 'SUCCESS' || query.state.data?.status === 'FAILURE') {
        return false; // Stop polling
      }
      return 1000; // Poll every 1s
    }
  });

  // Watch for Success
  useEffect(() => {
    if (taskStatus?.status === 'SUCCESS' && taskStatus.result) {
      const result = taskStatus.result;
      setOptimizationMetrics(result);

      // Map Indices (Strings) back to Addresses
      // We rely on the 'stops' state which drove the request
      const indices = result.optimized_order.map((i: string) => parseInt(i));

      // Reconstruct the full list used for indexing (Depot + Stops)
      // Logic mirrors backend assumption: 0 is Depot if present
      // We already built this into 'stops' state in the first useEffect

      const orderedAddresses = indices.map((i: number) => stops[i]?.address).filter(Boolean);
      setOptimizedOrder(orderedAddresses);

      toast.success("Route optimized successfully!", {
        description: `Total Distance: ${result.total_distance_km} km`
      });
    } else if (taskStatus?.status === 'FAILURE') {
      toast.error("Optimization failed. Please check inputs.");
    }
  }, [taskStatus, stops]);

  const handleOptimize = () => {
    try {
      const parsed = JSON.parse(jsonInput);
      // Validate structure minimally
      if (!parsed.stops && !Array.isArray(parsed)) {
        toast.error("Invalid JSON format: missing 'stops' array");
        return;
      }
      optimizeMutation.mutate(parsed);
    } catch (e) {
      toast.error("Invalid JSON syntax");
    }
  };

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden">
      {/* Sidebar */}
      <aside className="w-[400px] border-r bg-card p-6 flex flex-col gap-6 overflow-y-auto z-10 shadow-xl">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2 text-primary">
            <Truck className="h-8 w-8" />
            SimpliRoute
          </h1>
          <p className="text-muted-foreground text-sm">High-Performance Engine</p>
        </div>

        <div className="space-y-4">
          <Label>Delivery Configuration (JSON)</Label>
          <textarea
            className="flex min-h-[250px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 font-mono"
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
          />
          <Button
            className="w-full"
            size="lg"
            onClick={handleOptimize}
            disabled={optimizeMutation.isPending || (taskId !== null && !optimizationMetrics)}
          >
            {optimizeMutation.isPending || (taskId && !optimizationMetrics) ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Optimizing Route...
              </>
            ) : (
              <>
                <Activity className="mr-2 h-4 w-4" />
                Optimize Route
              </>
            )}
          </Button>
        </div>

        {/* Results Area */}
        {metricsCard(optimizationMetrics, optimizedOrder)}

      </aside>

      {/* Main Map Area */}
      <main className="flex-1 relative bg-slate-100">
        <MapComponent stops={stops} optimizedOrder={optimizedOrder} />

        {/* Floating Legend / Status */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur p-4 rounded-lg shadow-lg border z-[500]">
          <h3 className="font-semibold flex items-center gap-2">
            <MapIcon className="h-4 w-4" />
            Live Map
          </h3>
          <div className="text-sm space-y-1 mt-2">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-500 block"></span>
              <span>Stops ({stops.length})</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500 block"></span>
              <span>Optimized Path</span>
            </div>
          </div>
        </div>
      </main>
      <Toaster />
    </div>
  );
}

function metricsCard(metrics: any, optimizedOrder: string[]) {
  if (!metrics) return null;

  // Use mapped addresses if available, otherwise raw indices
  const displaySteps = (optimizedOrder && optimizedOrder.length > 0) ? optimizedOrder : metrics.optimized_order;

  return (
    <Card className="animate-in fade-in slide-in-from-bottom-4 duration-500">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">Optimization Results</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <Label className="text-xs text-muted-foreground">Total Distance</Label>
            <div className="text-2xl font-bold">{metrics.total_distance_km} km</div>
          </div>
          <div className="space-y-1">
            <Label className="text-xs text-muted-foreground">Est. Time</Label>
            <div className="text-2xl font-bold flex items-center gap-1">
              <Clock className="h-5 w-5 text-muted-foreground" />
              {(() => {
                const total = metrics.estimated_travel_time_minutes;
                const h = Math.floor(total / 60);
                const m = Math.round(total % 60);
                return h > 0 ? `${h}h ${m}m` : `${m}m`;
              })()}
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <Label className="text-xs text-muted-foreground">Optimal Sequence</Label>
          <div className="max-h-[150px] overflow-y-auto text-sm space-y-1 border rounded p-2 bg-muted/50">
            {displaySteps.map((step: string, i: number) => (
              <div key={i} className="flex gap-2">
                <span className="font-mono text-muted-foreground">{i + 1}.</span>
                <span>{step}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default App;
