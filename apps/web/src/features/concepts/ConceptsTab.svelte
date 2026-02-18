<script lang="ts">
  import type { ConceptsSettings } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';
  import Input from '../../lib/components/ui/Input.svelte';
  import Label from '../../lib/components/ui/Label.svelte';
  import Select from '../../lib/components/ui/Select.svelte';
  import Switch from '../../lib/components/ui/Switch.svelte';

  export let conceptsForm: ConceptsSettings;
  export let conceptTypes: string[] = [];
  export let balancingStrategies: string[] = [];
  export let promptSources: string[] = [];
  export let saving = false;
  export let onSubmit: (event: SubmitEvent) => void | Promise<void>;
  export let onReload: () => void | Promise<void>;
  export let addConcept: () => void;
  export let removeConcept: (index: number) => void;
</script>

<form class="general-form" on:submit={onSubmit}>
  <div class="field-grid">
    <div class="field-row full-width">
      <Label forId="concept_file_name">Concept Config File</Label>
      <Input name="concept_file_name" bind:value={conceptsForm.concept_file_name} />
    </div>

    <div class="field-row full-width">
      <Button type="button" disabled={saving} on:click={addConcept}>Add Concept</Button>
    </div>

    {#each conceptsForm.concepts as concept, i}
      <div class="field-row full-width">
        <div class="concept-header">
          <strong>Concept {i + 1}</strong>
          <Button type="button" disabled={saving} on:click={() => removeConcept(i)}>Remove</Button>
        </div>

        <div class="concept-grid">
          <div>
            <Label forId={`concept_name_${i}`}>Name</Label>
            <Input name={`concept_name_${i}`} bind:value={concept.name} />
          </div>

          <div>
            <Label forId={`concept_type_${i}`}>Concept Type</Label>
            <Select name={`concept_type_${i}`} bind:value={concept.type} options={conceptTypes} />
          </div>

          <div class="concept-full">
            <Label forId={`concept_path_${i}`}>Path</Label>
            <Input name={`concept_path_${i}`} bind:value={concept.path} />
          </div>

          <div>
            <Label forId={`concept_prompt_source_${i}`}>Prompt Source</Label>
            <Select name={`concept_prompt_source_${i}`} bind:value={concept.text.prompt_source} options={promptSources} />
          </div>

          <div>
            <Label forId={`concept_prompt_path_${i}`}>Prompt Path</Label>
            <Input name={`concept_prompt_path_${i}`} bind:value={concept.text.prompt_path} />
          </div>

          <div>
            <Label forId={`concept_balancing_${i}`}>Balancing</Label>
            <Input type="number" min={0} name={`concept_balancing_${i}`} bind:value={concept.balancing} />
          </div>

          <div>
            <Label forId={`concept_balancing_strategy_${i}`}>Balancing Strategy</Label>
            <Select name={`concept_balancing_strategy_${i}`} bind:value={concept.balancing_strategy} options={balancingStrategies} />
          </div>

          <div>
            <Label forId={`concept_loss_weight_${i}`}>Loss Weight</Label>
            <Input type="number" min={0} name={`concept_loss_weight_${i}`} bind:value={concept.loss_weight} />
          </div>

          <div>
            <Label forId={`concept_image_variations_${i}`}>Image Variations</Label>
            <Input type="number" min={1} name={`concept_image_variations_${i}`} bind:value={concept.image_variations} />
          </div>

          <div>
            <Label forId={`concept_text_variations_${i}`}>Text Variations</Label>
            <Input type="number" min={1} name={`concept_text_variations_${i}`} bind:value={concept.text_variations} />
          </div>

          <div class="switch-inline">
            <Label forId={`concept_enabled_${i}`}>Enabled</Label>
            <Switch name={`concept_enabled_${i}`} bind:checked={concept.enabled} />
          </div>

          <div class="switch-inline">
            <Label forId={`concept_include_subdirectories_${i}`}>Include Subdirectories</Label>
            <Switch name={`concept_include_subdirectories_${i}`} bind:checked={concept.include_subdirectories} />
          </div>
        </div>
      </div>
    {/each}
  </div>

  <div class="action-row">
    <Button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save Concept Settings'}</Button>
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</form>
