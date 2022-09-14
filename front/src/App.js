import { useEffect, useState } from 'react'
import axios from 'axios'
import { Header } from './components/Header'
import { Chart } from './components/Chart'
import { Total } from './components/Total'
import { ListOrders } from './components/ListOrders'

function App() {
  const [orders, setOrders] = useState([])
  const [total, setTotal] = useState(0)
  // const [limit, setLimit] = useState(50)



  useEffect(() => {
      axios.get(
        `http://localhost:5000/orders/`
      ).then((resp) => {
        setOrders(resp.data);
      })
  },[setOrders])

  useEffect(() => {
    if(orders.length > 0){
      let prices = [];
      for(let i = 0; i < orders.length; i++){
        prices.push(Number(orders[i].price_dollars));
      }
      setTotal(prices.reduce((a, b) => a + b,0))
    }
  }, [orders])

  
  return (
    <>
      <Header/>
      <div className='container'>
        <div className='left_container'>
          <Chart orders={orders}/>
        </div>
        <div className='right_container'>
          <Total total={total}/>
          <ListOrders orders={orders}/>
        </div>
      </div>
    </>
  );
}

export default App;
