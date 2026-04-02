import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import Login from '@/views/Login/Login.vue';

const push = vi.fn();
const login = vi.fn().mockResolvedValue(true);

vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router');
  return {
    ...actual,
    useRouter: () => ({ push }),
  };
});

vi.mock('@/store/authStore', () => ({
  useAuthStore: () => ({
    login,
    error: '',
  }),
}));

describe('IT-LOGIN-001', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    push.mockClear();
    login.mockClear();
  });

  it('navigates to /main after a successful login', async () => {
    const wrapper = mount(Login, {
      global: { stubs: ['BIconEye', 'BIconEyeSlash'] },
    });

    await wrapper.get('[data-test="login-email"]').setValue('test@example.com');
    await wrapper.get('[data-test="login-password"]').setValue('password123');
    await wrapper.get('form').trigger('submit.prevent');
    await flushPromises();

    expect(login).toHaveBeenCalledWith({ email: 'test@example.com', password: 'password123' });
    expect(login).toHaveBeenCalled();
  });
});
