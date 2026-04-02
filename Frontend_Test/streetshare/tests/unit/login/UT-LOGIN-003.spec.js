import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import Login from '@/views/Login/Login.vue';

const push = vi.fn();
vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router');
  return {
    ...actual,
    useRouter: () => ({ push }),
  };
});

describe('UT-LOGIN-003', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('enables the submit button only when both fields are filled', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: ['BIconEye', 'BIconEyeSlash'],
      },
    });

    const emailInput = wrapper.get('[data-test="login-email"]');
    const passwordInput = wrapper.get('[data-test="login-password"]');
    const submitButton = wrapper.get('[data-test="login-submit"]');

    expect(submitButton.attributes('disabled')).toBeDefined();

    await emailInput.setValue('test@example.com');
    expect(submitButton.attributes('disabled')).toBeDefined();

    await passwordInput.setValue('securePass123');
    expect(submitButton.attributes('disabled')).toBeUndefined();

    await emailInput.setValue('');
    expect(submitButton.attributes('disabled')).toBeDefined();
  });
});
