import { BrowserRouter, Routes, Route, Navigate, Link} from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/Login/LoginPage';
import CarsPage from './pages/Cars/CarsPage';
import OrdersPage from './pages/Orders';
import OrderDetailPage from './pages/OrderDetail';
import ProfilePage from './pages/Profile';
import WorksPage from './pages/Works';
import CreateOrderPage from './pages/CreateOrder/CreateOrderPage';

function App() {
  const { token, logout } = useAuth();

  return (
    <BrowserRouter>
      {!token ? (
        // Неавторизован — только логин
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      ) : (
        // Авторизован — все страницы
        <div style={{ display: 'flex' }}>
          {/* Навигация */}
          <nav style={{ width: '200px', padding: '20px', borderRight: '1px solid #ccc' }}>
            <h3>CRM</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><Link to="/cars">Машины</Link></li>
              <li><Link to="/profile">Профиль</Link></li>
              <li><Link to="/works">Работы</Link></li>
              <li><Link to="/orders">Заказы</Link></li>
              {/* <li><Link to="/create-order">Создать заказ</Link></li> */}
              <li><button onClick={logout}>Выйти</button></li>
            </ul>
          </nav>

          {/* Контент */}
          <div style={{ flex: 1, padding: '20px' }}>
            <Routes>
              <Route path="/cars" element={<CarsPage />} />
              <Route path="/orders" element={<OrdersPage />} />
              <Route path="/orders/:id" element={<OrderDetailPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/works" element={<WorksPage />} />
              <Route path="/create-order" element={<CreateOrderPage />} />
              <Route path="*" element={<Navigate to="/cars" replace />} />
            </Routes>
          </div>
        </div>
      )}
    </BrowserRouter>
  );
}

export default App;