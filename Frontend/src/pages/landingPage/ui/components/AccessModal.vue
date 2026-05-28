<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal" @click="handleBackdropClick">
      <div class="modal-content" @click.stop>
        <i class="fas fa-chart-network modal-icon"></i>
        <h3>Acceso Corporativo</h3>
        <p>Ingrese sus credenciales para acceder al simulador de optimización.</p>
        
        <input
          v-model="userName"
          type="text"
          placeholder="Nombre / Empresa"
        />
        <input
          v-model="userEmail"
          type="email"
          placeholder="Correo institucional"
        />
        
        <div class="modal-buttons">
          <button class="btn-modal btn-modal-cancel" @click="handleClose">
            Cancelar
          </button>
          <button class="btn-modal btn-modal-confirm" @click="handleConfirm">
            Ingresar a Plataforma
          </button>
        </div>
        
        <p class="modal-footer">* Datos no almacenados · Demo académica de IO</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isOpen = ref(false);
const userName = ref('Logística Ejecutiva');
const userEmail = ref('operaciones@optilog.bo');

const open = () => {
  isOpen.value = true;
};

const handleClose = () => {
  isOpen.value = false;
};

const handleBackdropClick = () => {
  handleClose();
};

const handleConfirm = () => {
  const name = userName.value.trim() || 'Ejecutivo';
  
  console.log(`✅ Acceso concedido: ${name}`);
  console.log(`📧 Correo: ${userEmail.value}`);
  
  handleClose();
  
  // Mensaje flotante
  const msg = document.createElement('div');
  msg.style.position = 'fixed';
  msg.style.bottom = '25px';
  msg.style.right = '25px';
  msg.style.backgroundColor = '#1e2a3a';
  msg.style.borderLeft = '4px solid #d4a373';
  msg.style.color = '#e8edf2';
  msg.style.padding = '14px 20px';
  msg.style.borderRadius = '12px';
  msg.style.zIndex = '3000';
  msg.style.fontSize = '0.8rem';
  msg.style.fontWeight = '500';
  msg.style.backdropFilter = 'blur(8px)';
  msg.innerHTML = '<i class="fas fa-check-circle" style="color:#d4a373;"></i> Demo ejecutiva disponible · Abra la aplicación principal para usar el mapa interactivo.';
  document.body.appendChild(msg);
  
  setTimeout(() => {
    msg.remove();
    router.push('/setup');
  }, 2000);
};

defineExpose({
  open,
  handleClose
});
</script>

<style scoped>
.modal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  z-index: 2000;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #11161f;
  border-radius: 1.8rem;
  max-width: 450px;
  width: 90%;
  padding: 2rem;
  text-align: center;
  border: 1px solid #2a3342;
  box-shadow: 0 25px 40px rgba(0, 0, 0, 0.5);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-icon {
  font-size: 3rem;
  color: #d4a373;
  display: block;
  margin-bottom: 1rem;
}

.modal-content h3 {
  font-size: 1.6rem;
  margin: 0.5rem 0;
  color: #ffffff;
}

.modal-content p {
  color: #a0abb9;
  margin-bottom: 1.5rem;
}

.modal-content input {
  width: 100%;
  padding: 12px;
  margin: 12px 0;
  border-radius: 40px;
  border: 1px solid #2a3342;
  background: #0a0f1a;
  color: white;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.modal-content input:focus {
  outline: none;
  border-color: #d4a373;
  box-shadow: 0 0 0 3px rgba(212, 163, 115, 0.1);
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-modal {
  flex: 1;
  padding: 12px;
  border-radius: 40px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  font-size: 0.9rem;
}

.btn-modal-cancel {
  background: #2a3342;
  color: #cbd5e6;
}

.btn-modal-cancel:hover {
  background: #3a434e;
}

.btn-modal-confirm {
  background: #d4a373;
  color: #0a0f1a;
}

.btn-modal-confirm:hover {
  background: #e0b082;
  transform: scale(1.02);
}

.modal-footer {
  font-size: 0.7rem;
  margin-top: 1rem;
  opacity: 0.6;
}
</style>
