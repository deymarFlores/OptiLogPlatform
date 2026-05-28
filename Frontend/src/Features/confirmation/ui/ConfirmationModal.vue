<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleCancel">
    <div class="modal-content">
      <div class="modal-header">
        <h4>
          <i :class="`fas ${icon}`"></i>
          {{ title }}
        </h4>
        <button class="btn-close" @click="handleCancel">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal-body">
        <p class="confirmation-message">{{ message }}</p>
      </div>

      <div class="modal-footer">
        <button class="btn-cancel" @click="handleCancel">{{ cancelText }}</button>
        <button :class="['btn-confirm', { dangerous: isDangerous }]" @click="handleConfirm">{{ confirmText }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirmación'
  },
  message: {
    type: String,
    default: '¿Estás seguro?'
  },
  icon: {
    type: String,
    default: 'fa-exclamation-triangle'
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  },
  isDangerous: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['confirm', 'cancel']);

const handleConfirm = () => {
  emit('confirm');
};

const handleCancel = () => {
  emit('cancel');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(6px);
}

.modal-content {
  background: rgba(18, 24, 34, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 163, 115, 0.2);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 420px;
  overflow: hidden;
}

.modal-header {
  background: rgba(212, 163, 115, 0.15);
  border-bottom: 1px solid rgba(212, 163, 115, 0.2);
  color: #ffffff;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #d4a373;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-close {
  background: rgba(212, 163, 115, 0.1);
  border: 1px solid rgba(212, 163, 115, 0.2);
  color: #d4a373;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.btn-close:hover {
  background: rgba(212, 163, 115, 0.2);
  border-color: rgba(212, 163, 115, 0.4);
}

.modal-body {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirmation-message {
  margin: 0;
  font-size: 1rem;
  color: #e8edf2;
  text-align: center;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-top: 1px solid rgba(212, 163, 115, 0.1);
  justify-content: flex-end;
}

.btn-cancel,
.btn-confirm {
  padding: 0.8rem 1.5rem;
  border: 1px solid rgba(212, 163, 115, 0.3);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-cancel {
  background: rgba(95, 125, 149, 0.1);
  color: #8fa3b3;
  border-color: rgba(95, 125, 149, 0.3);
}

.btn-cancel:hover {
  background: rgba(95, 125, 149, 0.2);
  border-color: rgba(95, 125, 149, 0.5);
  color: #a8b9c5;
}

.btn-confirm {
  background: rgba(212, 163, 115, 0.2);
  color: #d4a373;
  border-color: rgba(212, 163, 115, 0.4);
}

.btn-confirm:hover {
  background: rgba(212, 163, 115, 0.35);
  border-color: rgba(212, 163, 115, 0.6);
  color: #e8c48e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 163, 115, 0.2);
}

.btn-confirm.dangerous {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.4);
}

.btn-confirm.dangerous:hover {
  background: rgba(239, 68, 68, 0.35);
  border-color: rgba(239, 68, 68, 0.6);
  color: #f87171;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-width: 90vw;
  }

  .modal-header {
    padding: 1.2rem;
  }

  .modal-header h4 {
    font-size: 1rem;
  }

  .modal-body {
    padding: 1.2rem;
  }

  .modal-footer {
    flex-direction: column;
    padding: 1.2rem;
  }

  .btn-cancel,
  .btn-confirm {
    width: 100%;
  }
}
</style>
