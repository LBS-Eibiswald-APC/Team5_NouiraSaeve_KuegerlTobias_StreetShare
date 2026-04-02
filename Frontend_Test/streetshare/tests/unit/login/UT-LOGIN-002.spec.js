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

describe('UT-LOGIN-002', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('accepts password strings and updates the ref value', async () => {
    const wrapper = mount(Login, {
      global: {
        stubs: ['BIconEye', 'BIconEyeSlash'],
      },
    });

    const passwordInput = wrapper.get('[data-test="login-password"]');
    await passwordInput.setValue('securePass123');

    expect(wrapper.vm.password).toBe('securePass123');
  });
});
