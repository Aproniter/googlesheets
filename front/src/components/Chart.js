import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
  } from "recharts";

  export function Chart({orders}) {
    return(
        <LineChart
            width={650}
            height={500}
            data={orders}
            margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5
            }}
            >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="delivery_time" />
      <YAxis dataKey="price_dollars"/>
      <Tooltip />
      <Legend />
      <Line
        type="monotone"
        dataKey="price_dollars"
        stroke="#8884d8"
        activeDot={{ r: 3 }}
      />
      
    </LineChart>
  );
  }