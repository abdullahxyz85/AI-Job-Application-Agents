import React from 'react';
import toast, { Toaster } from 'react-hot-toast';

export const showToast = {
  success: (message: string) => toast.success(message, {
    duration: 4000,
    style: {
      background: '#10B981',
      color: '#fff',
    },
  }),
  error: (message: string) => toast.error(message, {
    duration: 4000,
    style: {
      background: '#EF4444',
      color: '#fff',
    },
  }),
  info: (message: string) => toast(message, {
    duration: 4000,
    icon: '🤖',
    style: {
      background: '#3B82F6',
      color: '#fff',
    },
  }),
};

export const ToastProvider: React.FC = () => {
  return (
    <Toaster
      position="top-right"
      reverseOrder={false}
      gutter={8}
      containerClassName=""
      containerStyle={{}}
      toastOptions={{
        className: '',
        duration: 4000,
        style: {
          borderRadius: '10px',
          fontSize: '14px',
        },
      }}
    />
  );
};