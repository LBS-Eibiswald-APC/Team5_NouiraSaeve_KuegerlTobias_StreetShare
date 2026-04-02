import { mount } from '@vue/test-utils';
import ToolCreate from '@/components/PopUp/ToolCreate.vue';

vi.mock('vue-toast-notification', () => ({ useToast: () => ({ success: vi.fn(), error: vi.fn() }) }));

describe('UT-TOOL-003', () => {
  it('calculates the deposit based on price and condition', async () => {
    const wrapper = mount(ToolCreate, {
      props: {
        showModal: true,
        newTool: { name: '', description: '', base_price: 0, tool_condition: 'Neu', deposit: 0 },
        usageFactor: { Neu: 0.35, 'Minimal abgenutzt': 0.3, Gebraucht: 0.25, 'Gut abgenutzt': 0.2, Defekt: 0.1 },
        week_multiplier: 1,
        toolStore: { createTool: vi.fn() },
      },
    });

    await wrapper.get('[data-test="tool-price"]').setValue('100');
    await wrapper.get('[data-test="tool-condition"]').setValue('Neu');

    const depositInput = wrapper.get('[data-test="tool-deposit"]');
    expect(Number(depositInput.element.value)).toBeGreaterThan(0);
  });
});
