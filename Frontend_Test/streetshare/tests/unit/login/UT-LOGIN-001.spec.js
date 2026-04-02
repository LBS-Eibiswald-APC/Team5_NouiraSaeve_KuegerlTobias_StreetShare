import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import Login from '@/views/Login/Login.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

const push = vi.fn();
vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router');
  return {
    ...actual,
    useRouter: () => ({ push }),
  };
});

describe('UT-LOGIN-001', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('accepts valid email addresses in the login form', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: ['BIconEye', 'BIconEyeSlash'],
      },
    });

    const emailInput = wrapper.get('[data-test="login-email"]');
    await emailInput.setValue('test@example.com');

    expect(wrapper.vm.email).toBe('test@example.com');
  });
});
