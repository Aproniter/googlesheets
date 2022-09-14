export function ListOrders({orders}) {
    
    return(
        <div className='list_orders'>
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Заказ №</th>
                        <th>Стоимость,$</th>
                        <th>Стоимость,RUB</th>
                        <th>Срок поставки</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map(
                        order =>
                            <tr key={order.order_id}>
                                <td>
                                    {order.order_id}
                                </td>
                                <td>
                                    {order.order_number}
                                </td>
                                <td>
                                    {order.price_dollars}
                                </td>
                                <td>
                                    {order.price_rub}
                                </td>
                                <td>
                                    {order.delivery_time}
                                </td>
                            </tr>
                    )}
                </tbody>
            </table>
        </div>
    )
}