<template>
  <div class="register-wrapper">
    <div class="bg-overlay"></div>
    <div class="bg-gradient"></div>

    <div class="auth-container">
      <div class="auth-card">
        <div class="logo-header">
          <i class="fas fa-chart-network"></i>
          <h1>OptiLog Executive</h1>
          <p>Crear cuenta corporativa</p>
        </div>

        <div class="auth-form">
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
              <label><i class="far fa-building"></i> Empresa / Organización</label>
              <input 
                v-model="registerForm.company"
                type="text" 
                placeholder="Logística Integral S.A." 
                required
              />
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
              <label for="acceptTerms">Acepto los <a href="#">términos y condiciones</a> y la política de privacidad</label>
            </div>
            <button type="submit" class="btn-auth"><i class="fas fa-user-plus"></i> Crear cuenta corporativa</button>
          </form>
          <p style="text-align: center; font-size:0.7rem; color:#7a8799; margin-top: 1rem;">
            Demo académica · Datos no almacenados persistentemente
          </p>
          <p style="text-align: center; font-size:0.8rem; color:#9aa5b5; margin-top: 1rem;">
            ¿Ya tienes cuenta? <router-link to="/login" style="color: #d4a373; cursor: pointer;">Inicia sesión aquí</router-link>
          </p>
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
const message = ref(null);

const registerForm = ref({
  fullname: '',
  company: '',
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

const showMessage = (text, isError = false) => {
  message.value = { text, isError };
  setTimeout(() => {
    message.value = null;
  }, 3500);
};

const handleRegister = () => {
  const { fullname, company, email, password, confirmPassword, terms } = registerForm.value;
  
  if (!fullname || !company || !email) {
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
  
  // Register user and redirect to setup (3 pasos: Empresa → Distribución → Productos)
  const newUser = { fullname, company, email, password };
  registeredUsers.value.push(newUser);
  showMessage(`🎉 Registro exitoso, ${fullname}. Iniciando configuración...`);
  
  setTimeout(() => {
    sessionStorage.setItem('newUserData', JSON.stringify({
      fullname,
      company
    }));
    router.push('/setup');
  }, 1500);
};
</script>

<style scoped>
.register-wrapper {
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

@media (max-width: 550px) {
  .auth-card {
    padding: 1.8rem;
  }
  .message-toast {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
  }
}
</style>