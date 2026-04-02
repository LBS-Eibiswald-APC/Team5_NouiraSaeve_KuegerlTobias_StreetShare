import { mount } from '@vue/test-utils';
import ToolCreate from '@/components/PopUp/ToolCreate.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

describe('UT-TOOL-001', () => {
  it('stores the tool name string correctly', async () => {
    const wrapper = mount(ToolCreate, {
      props: {
        showModal: true,
        newTool: { name: '', description: '', base_price: 0, tool_condition: 'Neu', deposit: 0 },
        usageFactor: { Neu: 0.35, 'Minimal abgenutzt': 0.3, Gebraucht: 0.25, 'Gut abgenutzt': 0.2, Defekt: 0.1 },
        week_multiplier: 1,
        toolStore: { createTool: vi.fn() },
      },
    });

    const nameInput = wrapper.get('[data-test="tool-name"]');
    await nameInput.setValue('Bohrmaschine');

    expect(wrapper.vm.localTool.name).toBe('Bohrmaschine');
  });
});
