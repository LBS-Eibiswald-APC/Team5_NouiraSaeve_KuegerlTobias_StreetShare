import { mount, flushPromises } from '@vue/test-utils';
import ToolCreate from '@/components/PopUp/ToolCreate.vue';

vi.mock('vue-toast-notification', () => ({
  useToast: () => ({ error: vi.fn(), success: vi.fn() })
}));

describe('IT-TOOL-001', () => {
  it('creates a new tool and closes the modal flow', async () => {
    const createTool = vi.fn().mockResolvedValue(true);

    const wrapper = mount(ToolCreate, {
      props: {
        showModal: true,
        newTool: {
          name: '',
          description: '',
          base_price: 0,
          tool_condition: 'Neu',
          deposit: 0
        },
        usageFactor: {
          Neu: 0.35,
          'Minimal abgenutzt': 0.3,
          Gebraucht: 0.25,
          'Gut abgenutzt': 0.2,
          Defekt: 0.1
        },
        week_multiplier: 1,
        toolStore: { createTool },
      },
    });

    await wrapper.get('[data-test="tool-name"]').setValue('Hammer');
    await wrapper.get('[data-test="tool-description"]').setValue('Starker Hammer');
    await wrapper.get('[data-test="tool-price"]').setValue('25');
    await wrapper.get('[data-test="tool-condition"]').setValue('Gut abgenutzt');

    const file = new File(['image'], 'tool.png', { type: 'image/png' });
    const fileInput = wrapper.get('[data-test="tool-image"]');

    Object.defineProperty(fileInput.element, 'files', {
      value: [file],
      writable: false,
    });

    await fileInput.trigger('change');

    await wrapper.get('[data-test="tool-submit"]').trigger('click');
    await flushPromises();

    expect(createTool).toHaveBeenCalled();
    expect(wrapper.emitted('saved')).toBeTruthy();
    expect(wrapper.emitted('close')).toBeTruthy();
  });
});