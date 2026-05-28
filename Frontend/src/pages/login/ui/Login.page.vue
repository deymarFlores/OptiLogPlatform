<template>
  <div class="login-wrapper">
    <div class="bg-overlay"></div>
    <div class="bg-gradient"></div>

    <div class="auth-container">
      <div class="auth-card">
        <div class="logo-header">
          <i class="fas fa-chart-network"></i>
          <h1>OptiLog Executive</h1>
          <p>Plataforma de Optimización Logística · Investigación Operativa</p>
        </div>

        <!-- Tabs Login / Register -->
        <div class="auth-tabs">
          <button class="tab-btn active" @click="switchTab('login')">Iniciar Sesión</button>
          <button class="tab-btn" @click="switchTab('register')">Registrarse</button>
        </div>

        <!-- FORMULARIO LOGIN -->
        <div v-show="activeTab === 'login'" class="auth-form active-form">
          <form @submit.prevent="handleLogin">
            <div class="input-group">
              <label><i class="far fa-envelope"></i> Correo electrónico</label>
              <input 
                v-model="loginForm.email"
                type="email" 
                placeholder="ejecutivo@optilog.bo" 
                required 
                autocomplete="email"
              />
            </div>
            <div class="input-group">
              <label><i class="fas fa-lock"></i> Contraseña</label>
              <input 
                v-model="loginForm.password"
                type="password" 
                placeholder="••••••••" 
                required 
                autocomplete="current-password"
              />
            </div>
            <div class="forgot-link">
              <a href="#" @click.prevent="showForgotMessage">¿Olvidó su contraseña?</a>
            </div>
            <div class="checkbox-group">
              <input v-model="loginForm.remember" type="checkbox" id="rememberMe">
              <label for="rememberMe">Mantener sesión iniciada</label>
            </div>
            <button type="submit" class="btn-auth"><i class="fas fa-arrow-right-to-bracket"></i> Acceder al Dashboard</button>
          </form>
          <div class="separator">
            <hr><span>O continuar con</span><hr>
          </div>
          <div class="social-buttons">
            <button type="button" class="social-btn" @click="socialLogin('google')"><i class="fab fa-google"></i> Google</button>
            <button type="button" class="social-btn" @click="socialLogin('linkedin')"><i class="fab fa-linkedin-in"></i> LinkedIn</button>
          </div>
          <div class="terms-text">
            Al iniciar sesión acepta los <a href="#">Términos de Servicio</a> y <a href="#">Política de Privacidad</a>.
          </div>
        </div>

        <!-- FORMULARIO REGISTER -->
        <div v-show="activeTab === 'register'" class="auth-form active-form">
          <form @submit.prevent="handleRegister">
            <div class="input-group">
              <label><i class="fas fa-user-tie"></i> Nombre completo</label>
              <input 
                v-model="registerForm.fullname"
                type="text" 
                placeholder="Carlos Mendoza" 
                required
              />
            </div>
            <div class="input-group">
              <label><i class="fas fa-user-tag"></i> Tipo de Cuenta</label>
              <select 
                v-model="registerForm.role"
                required
                class="role-select"
              >
                <option value="">Seleccionar tipo de cuenta...</option>
                <option value="empresa">Empresa / Organización</option>
                <option value="cliente">Cliente</option>
              </select>
            </div>
            <div class="input-group">
              <label><i class="far fa-envelope"></i> Correo electrónico</label>
              <input 
                v-model="registerForm.email"
                type="email" 
                placeholder="contacto@empresa.bo" 
                required
              />
            </div>
            <div class="input-group">
              <label><i class="fas fa-lock"></i> Contraseña</label>
              <input 
                v-model="registerForm.password"
                type="password" 
                placeholder="••••••••" 
                required
              />
            </div>
            <div class="input-group">
              <label><i class="fas fa-check-circle"></i> Confirmar contraseña</label>
              <input 
                v-model="registerForm.confirmPassword"
                type="password" 
                placeholder="••••••••" 
                required
              />
            </div>
            <div class="checkbox-group">
              <input v-model="registerForm.terms" type="checkbox" id="acceptTerms" required>
              <label for="acceptTerms">Acepto los <a href="#" style="color:#d4a373;">términos y condiciones</a> y la política de privacidad</label>
            </div>
            <button type="submit" class="btn-auth"><i class="fas fa-user-plus"></i> Crear cuenta</button>
          </form>
          <div class="separator">
            <hr><span>Registro corporativo</span><hr>
          </div>
          <p style="text-align: center; font-size:0.7rem; color:#7a8799;">Demo académica · Datos no almacenados persistentemente</p>
        </div>
      </div>
    </div>

    <!-- Toast message -->
    <div v-if="message" :class="['message-toast', { error: message.isError }]">
      <i :class="['fas', message.isError ? 'fa-exclamation-triangle' : 'fa-check-circle']"></i>
      {{ message.text }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeTab = ref('login');
const message = ref(null);

const loginForm = ref({
  email: '',
  password: '',
  remember: false
});

const registerForm = ref({
  fullname: '',
  role: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: false
});

const registeredUsers = ref([
  {
    fullname: "Ana Rojas",
    company: "Distribuciones Andinas",
    email: "ana@distribuciones.bo",
    password: "Andinas123"
  }
]);

const DEMO_CREDENTIALS = {
  email: "ejecutivo@optilog.bo",
  password: "OptiLog2025"
};

const switchTab = (tab) => {
  activeTab.value = tab;
};

const showMessage = (text, isError = false) => {
  message.value = { text, isError };
  setTimeout(() => {
    message.value = null;
  }, 3500);
};

const handleLogin = () => {
  const { email, password } = loginForm.value;
  
  const isDemoValid = (email === DEMO_CREDENTIALS.email && password === DEMO_CREDENTIALS.password);
  const registeredUser = registeredUsers.value.find(user => user.email === email && user.password === password);
  
  if (isDemoValid) {
    const userName = "Ejecutivo Principal";
    showMessage(`✅ Acceso concedido. Bienvenido ${userName}. Redirigiendo al dashboard...`);
    setTimeout(() => {
      // LOGIN Demo: Ir a dashboard de empresa
      router.push('/dashboard');
    }, 1500);
  } else if (registeredUser) {
    const userName = registeredUser.fullname;
    const role = registeredUser.role || 'empresa'; // Default a empresa
    
    showMessage(`✅ Acceso concedido. Bienvenido ${userName}. Redirigiendo...`);
    setTimeout(() => {
      sessionStorage.setItem('currentUserData', JSON.stringify({
        fullname: userName,
        role
      }));
      
      if (role === 'empresa') {
        router.push('/dashboard');
      } else {
        router.push('/client-dashboard');
      }
    }, 1500);
  } else {
    showMessage("❌ Credenciales incorrectas. Use ejecutivo@optilog.bo / OptiLog2025 o registre una cuenta.", true);
  }
};

const handleRegister = () => {
  const { fullname, role, email, password, confirmPassword, terms } = registerForm.value;
  
  if (!fullname || !role || !email) {
    showMessage("Por favor complete todos los campos requeridos.", true);
    return;
  }
  
  if (password !== confirmPassword) {
    showMessage("Las contraseñas no coinciden.", true);
    return;
  }
  
  if (password.length < 6) {
    showMessage("La contraseña debe tener al menos 6 caracteres.", true);
    return;
  }
  
  if (!terms) {
    showMessage("Debe aceptar los términos y condiciones.", true);
    return;
  }
  
  if (registeredUsers.value.some(u => u.email === email)) {
    showMessage("Este correo ya está registrado. Inicie sesión.", true);
    return;
  }
  
  // Register user and redirect based on role
  const newUser = { fullname, role, email, password };
  registeredUsers.value.push(newUser);
  
  if (role === 'empresa') {
    showMessage(`🎉 Registro exitoso, ${fullname}. Iniciando configuración de empresa...`);
    setTimeout(() => {
      // Empresa: Redirige a /setup para configuración inicial (3 pasos)
      sessionStorage.setItem('newUserData', JSON.stringify({
        fullname,
        role
      }));
      router.push('/setup');
    }, 1500);
  } else {
    showMessage(`🎉 Registro exitoso, ${fullname}. Redirigiendo a tu panel de cliente...`);
    setTimeout(() => {
      // Cliente: Redirige a /client-dashboard
      sessionStorage.setItem('newUserData', JSON.stringify({
        fullname,
        role
      }));
      router.push('/client-dashboard');
    }, 1500);
  }
};

const showForgotMessage = () => {
  showMessage("📧 Instrucciones de recuperación enviadas a su correo corporativo (simulación académica).");
};

const socialLogin = (provider) => {
  if (provider === 'google') {
    showMessage("🔐 Autenticación con Google (Demo). En entorno real se integraría OAuth.");
  } else {
    showMessage("🏢 Autenticación con LinkedIn (Demo corporativa). Redirigiendo al portal.");
  }
};
</script>

<style scoped>
.login-wrapper {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: #0a0f1a;
  color: #e8edf2;
  overflow-x: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -2;
  background-image: url('https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?q=80&w=2070&auto=format');
  background-size: cover;
  background-position: center 30%;
  filter: brightness(0.28) contrast(1.05);
}

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(135deg, rgba(10,15,26,0.94) 0%, rgba(20,28,40,0.88) 100%);
  backdrop-filter: blur(3px);
}

.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  z-index: 1;
}

.auth-card {
  background: rgba(15, 21, 30, 0.85);
  backdrop-filter: blur(16px);
  border-radius: 2rem;
  border: 1px solid rgba(212, 163, 115, 0.25);
  width: 100%;
  max-width: 480px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
  transition: all 0.3s ease;
}

.logo-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-header i {
  font-size: 2.8rem;
  color: #d4a373;
  background: rgba(212, 163, 115, 0.12);
  padding: 1rem;
  border-radius: 1.5rem;
}

.logo-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-top: 1rem;
  background: linear-gradient(135deg, #ffffff, #d4a373);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.logo-header p {
  font-size: 0.85rem;
  color: #9aa5b5;
  margin-top: 0.5rem;
}

.auth-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  padding-bottom: 0.5rem;
}

.tab-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 0.8rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  color: #8e9aab;
  transition: all 0.2s;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
}

.tab-btn.active {
  color: #d4a373;
  background: rgba(212, 163, 115, 0.1);
}

.tab-btn:hover:not(.active) {
  color: #cbd5e6;
  background: rgba(255,255,255,0.03);
}

.auth-form {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #b0bdcc;
}

.input-group input {
  width: 100%;
  padding: 0.9rem 1rem;
  background: rgba(10, 15, 26, 0.7);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 1rem;
  color: #ffffff;
  font-size: 0.9rem;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.input-group input:focus {
  outline: none;
  border-color: #d4a373;
  background: rgba(10, 15, 26, 0.9);
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.input-group input::placeholder {
  color: #5a6678;
}

.role-select {
  width: 100%;
  padding: 0.9rem 1rem;
  background: rgba(10, 15, 26, 0.7);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 1rem;
  color: #ffffff;
  font-size: 0.9rem;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
}

.role-select:focus {
  outline: none;
  border-color: #d4a373;
  background: rgba(10, 15, 26, 0.9);
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.role-select option {
  background: #0a0f1a;
  color: #ffffff;
  padding: 0.5rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.checkbox-group input {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #d4a373;
}

.checkbox-group label {
  font-size: 0.8rem;
  color: #b0bdcc;
  cursor: pointer;
}

.checkbox-group a {
  color: #d4a373;
  text-decoration: none;
}

.checkbox-group a:hover {
  text-decoration: underline;
}

.btn-auth {
  width: 100%;
  padding: 0.9rem;
  background: #d4a373;
  border: none;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 0.95rem;
  color: #0a0f1a;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  margin-top: 0.5rem;
}

.btn-auth:hover {
  background: #e0b082;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 163, 115, 0.3);
}

.forgot-link {
  text-align: right;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
}

.forgot-link a {
  color: #9aa5b5;
  font-size: 0.75rem;
  text-decoration: none;
  transition: 0.2s;
}

.forgot-link a:hover {
  color: #d4a373;
}

.separator {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
  color: #5a6678;
  font-size: 0.7rem;
}

.separator hr {
  flex: 1;
  border: none;
  height: 1px;
  background: rgba(255,255,255,0.08);
}

.social-buttons {
  display: flex;
  gap: 1rem;
}

.social-btn {
  flex: 1;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  padding: 0.7rem;
  border-radius: 1rem;
  cursor: pointer;
  transition: 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  color: #cbd5e6;
  font-size: 0.8rem;
  font-family: 'Inter', sans-serif;
}

.social-btn:hover {
  background: rgba(212, 163, 115, 0.1);
  border-color: rgba(212, 163, 115, 0.3);
}

.social-btn i {
  font-size: 1.1rem;
}

.message-toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #1e2a3a;
  border-left: 4px solid #d4a373;
  padding: 1rem 1.5rem;
  border-radius: 0.8rem;
  color: #e8edf2;
  font-size: 0.85rem;
  z-index: 2000;
  backdrop-filter: blur(8px);
  animation: slideInRight 0.3s ease;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.message-toast.error {
  border-left-color: #e06c6c;
}

@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.terms-text {
  font-size: 0.7rem;
  text-align: center;
  margin-top: 1.5rem;
  color: #6c7a8e;
}

.terms-text a {
  color: #d4a373;
  text-decoration: none;
}

@media (max-width: 550px) {
  .auth-card {
    padding: 1.8rem;
  }
  .social-buttons {
    flex-direction: column;
  }
  .message-toast {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
  }
}
</style>