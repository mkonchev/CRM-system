import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/Login/LoginPage';
import CarsPage from './pages/Cars/CarsPage';
import OrdersPage from './pages/Orders/OrdersPage';
import OrderDetailPage from './pages/OrderDetail/OrderDetailPage';
import ProfilePage from './pages/Profile/ProfilePage';
import WorksPage from './pages/Works/WorksPage';
import CreateOrderPage from './pages/CreateOrder/CreateOrderPage';
import RegisterPage from './pages/Register/RegisterPage';

function App() {
  const { token, logout } = useAuth();

  return (
    <BrowserRouter>
      {!token ? (
        <div style={{ display: 'flex' }}>
          <nav style={{ width: '200px', padding: '20px', borderRight: '1px solid #ccc' }}>
            <h3>CRM</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><Link to="/works">Работы</Link></li>
              <li><Link to="/login">Войти</Link></li>
            </ul>
          </nav>

          <div style={{ flex: 1, padding: '20px' }}>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/works" element={<WorksPage />} />
              <Route path="*" element={<Navigate to="/works" replace />} />
            </Routes>
          </div>
        </div>
      ) : (
        // Авторизован — все страницы
        <div style={{ display: 'flex' }}>
          <nav style={{ width: '200px', padding: '20px', borderRight: '1px solid #ccc' }}>
            <h3>CRM</h3>
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li><Link to="/cars">Машины</Link></li>
              <li><Link to="/profile">Профиль</Link></li>
              <li><Link to="/works">Работы</Link></li>
              <li><Link to="/orders">Заказы</Link></li>
              <li><button onClick={logout}>Выйти</button></li>
            </ul>
          </nav>

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