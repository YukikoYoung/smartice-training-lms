import React from 'react';

export interface FormInputProps {
  label: string;
  name: string;
  type?: 'text' | 'password' | 'email' | 'number' | 'tel' | 'url';
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  helpText?: string;
  maxLength?: number;
  minLength?: number;
  pattern?: string;
  autoComplete?: string;
  className?: string;
}

/**
 * 统一的表单输入框组件
 *
 * @example
 * <FormInput
 *   label="用户名"
 *   name="username"
 *   value={username}
 *   onChange={(e) => setUsername(e.target.value)}
 *   required
 *   error={errors.username}
 * />
 */
export const FormInput: React.FC<FormInputProps> = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  error,
  helpText,
  maxLength,
  minLength,
  pattern,
  autoComplete,
  className = '',
}) => {
  const inputId = `form-input-${name}`;

  return (
    <div className={`form-group ${className}`}>
      <label htmlFor={inputId} className="form-label">
        {label}
        {required && <span className="required-mark">*</span>}
      </label>

      <input
        id={inputId}
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        maxLength={maxLength}
        minLength={minLength}
        pattern={pattern}
        autoComplete={autoComplete}
        className={`form-control ${error ? 'is-invalid' : ''} ${disabled ? 'is-disabled' : ''}`}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : helpText ? `${inputId}-help` : undefined}
      />

      {error && (
        <div id={`${inputId}-error`} className="error-message" role="alert">
          {error}
        </div>
      )}

      {!error && helpText && (
        <div id={`${inputId}-help`} className="help-text">
          {helpText}
        </div>
      )}

      <style>{`
        .form-group {
          margin-bottom: 20px;
        }

        .form-label {
          display: block;
          margin-bottom: 8px;
          font-weight: 500;
          font-size: 14px;
          color: #333;
        }

        .required-mark {
          color: #e53e3e;
          margin-left: 4px;
        }

        .form-control {
          width: 100%;
          padding: 10px 12px;
          font-size: 14px;
          line-height: 1.5;
          color: #333;
          background-color: #fff;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }

        .form-control:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .form-control:hover:not(:disabled) {
          border-color: #9ca3af;
        }

        .form-control.is-invalid {
          border-color: #e53e3e;
        }

        .form-control.is-invalid:focus {
          border-color: #e53e3e;
          box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1);
        }

        .form-control.is-disabled {
          background-color: #f3f4f6;
          cursor: not-allowed;
          opacity: 0.6;
        }

        .error-message {
          margin-top: 6px;
          font-size: 13px;
          color: #e53e3e;
          display: flex;
          align-items: center;
        }

        .error-message::before {
          content: "⚠ ";
          margin-right: 4px;
        }

        .help-text {
          margin-top: 6px;
          font-size: 13px;
          color: #6b7280;
        }

        /* 移动端优化 */
        @media (max-width: 640px) {
          .form-control {
            font-size: 16px; /* 防止iOS自动缩放 */
            padding: 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default FormInput;
