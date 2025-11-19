import React from 'react';

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
}

export interface FormSelectProps {
  label: string;
  name: string;
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  options: SelectOption[];
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  helpText?: string;
  className?: string;
}

/**
 * 统一的下拉选择组件
 *
 * @example
 * <FormSelect
 *   label="部门"
 *   name="department"
 *   value={department}
 *   onChange={(e) => setDepartment(e.target.value)}
 *   options={[
 *     { value: 'FRONT_HALL', label: '前厅' },
 *     { value: 'KITCHEN', label: '厨房' },
 *   ]}
 *   required
 * />
 */
export const FormSelect: React.FC<FormSelectProps> = ({
  label,
  name,
  value,
  onChange,
  options,
  placeholder = '请选择',
  required = false,
  disabled = false,
  error,
  helpText,
  className = '',
}) => {
  const selectId = `form-select-${name}`;

  return (
    <div className={`form-group ${className}`}>
      <label htmlFor={selectId} className="form-label">
        {label}
        {required && <span className="required-mark">*</span>}
      </label>

      <div className="select-wrapper">
        <select
          id={selectId}
          name={name}
          value={value}
          onChange={onChange}
          required={required}
          disabled={disabled}
          className={`form-select ${error ? 'is-invalid' : ''} ${disabled ? 'is-disabled' : ''}`}
          aria-invalid={!!error}
          aria-describedby={error ? `${selectId}-error` : helpText ? `${selectId}-help` : undefined}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value} disabled={option.disabled}>
              {option.label}
            </option>
          ))}
        </select>

        <div className="select-arrow">
          <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
            <path d="M1 1L6 6L11 1" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>

      {error && (
        <div id={`${selectId}-error`} className="error-message" role="alert">
          {error}
        </div>
      )}

      {!error && helpText && (
        <div id={`${selectId}-help`} className="help-text">
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

        .select-wrapper {
          position: relative;
        }

        .form-select {
          width: 100%;
          padding: 10px 36px 10px 12px;
          font-size: 14px;
          line-height: 1.5;
          color: #333;
          background-color: #fff;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          cursor: pointer;
          appearance: none;
          transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }

        .form-select:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .form-select:hover:not(:disabled) {
          border-color: #9ca3af;
        }

        .form-select.is-invalid {
          border-color: #e53e3e;
        }

        .form-select.is-invalid:focus {
          border-color: #e53e3e;
          box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1);
        }

        .form-select.is-disabled {
          background-color: #f3f4f6;
          cursor: not-allowed;
          opacity: 0.6;
        }

        .select-arrow {
          position: absolute;
          top: 50%;
          right: 12px;
          transform: translateY(-50%);
          pointer-events: none;
          color: #6b7280;
          transition: transform 0.2s;
        }

        .form-select:focus + .select-arrow {
          color: #3b82f6;
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
          .form-select {
            font-size: 16px; /* 防止iOS自动缩放 */
            padding: 12px 36px 12px 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default FormSelect;
