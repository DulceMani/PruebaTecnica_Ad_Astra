<template>
  <div :class="bg_zone">
    <div v-if="display" class="zone-display">
      <!--se agrega updated at: {{ zone.updated_at }} para mostrar la fecha-->
      <div>
        Zone Name: <strong>{{ zone.name }}</strong> updated at: {{ zone.updated_at }} Distributions: {{
          distributionDisplay }}
      </div>

      <button class="btn btn-primary" @click="setDisplay(false)" :disabled="saving">
        Edit
      </button>
    </div>
    <div v-else class="zone-edit">
      <label class="control-label">
        Zone Name
      </label>
      <!--se agrega @keyup="filterKey_space" para eliminar espacios dobles-->
      <input v-model="form.name" placeholder="Zone name" class="form-control" :disabled="saving" @keyup="filterKey_space">

      <div class="zone-edit-distributions">
        <div v-for="distribution in form.distributions">
          <label class="control-label">
            Distribution
          </label>
          <div class="row m-1">
            <div class="col-10">
              <!--se agrega @keydown="filterKey_number" para validar que solo introdusca numeros-->
              <input type="text" v-model="distribution.percentage" placeholder="Percentage" class="form-control"
                 @keydown="filterKey_number">
            </div>
            <!--Nuevo boton para eliminar Distribution-->
            <button class="btn btn-danger col-2" @click="removeDistibition(distribution.id)">Remove</button>
          </div>

        </div>


      </div>
      <!--Nuevo boton para agregar Distribution-->
      <div class="row m-3">
        <button class="btn btn-info col-2" @click="newDistribution">New Distribution</button>
      </div>

      <div class="zone-edit-actions">
        <!--Se agrega @click="setDisplay(true) -->
        <button class="btn btn-secondary" :disabled="saving" @click="setDisplay(true)">
          Cancel
        </button>

        <button class="btn btn-success" @click="save" :disabled="saving">
          {{ btn_saving }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ZoneEditable',
  props: {
    zone: Object
    /*name: String,
    id: Number,
    distributions: Array,*/
  },
  data() {
    return {
      display: true,
      form: {
        name: '',
        distributions: [],
      },
      saving: false,
      btn_saving: 'Save',
      bg_zone: "zone-editable ",
    };
  },
  computed: {
    distributionDisplay() {
      return this.zone.distributions.map(distribution => '%' + distribution.percentage).join('-');
    }
  },
  mounted() {
    this.getValuesFromProps();
    this.change_bg_zone();
  },
  methods: {
    getValuesFromProps() {
      this.form.name = this.zone.name;
      /*this.form.distributions = this.zone.distributions.map(distribution => {
        return {
          id: distribution.id,
          percentage: distribution.percentage
        };
      });*/
      this.form.distributions = this.zone.distributions
    },
    change_bg_zone() {
      // se cambia fondo si hay 5 o mas distributions
      if (this.form.distributions.length >= 5) {
        this.bg_zone = "zone-editable bg-warning"
      } else {
        this.bg_zone = "zone-editable"
      }
    },
    setDisplay(value) {
      this.display = value;

      if (!this.display) {
        this.getValuesFromProps();
      }
    },
    async save() {
      this.saving = true;

      const params = {
        id: this.zone.id,
        name: this.form.name.trim(),// se quitan espacios al inicio y fin
        distributions: this.form.distributions
      };
      // se hacen validaciones 
      if (this.formValidations()) {
        this.$toasted.show('Saving...').goAway(1500);
        this.btn_saving = 'Saving...'
        this.saving = true;
        let resp = await axios.post('/api/zones/edit/', params);
        this.btn_saving = 'Save'

        if (resp.data.success) {
          this.$emit('edit', { zone: resp.data.zone });
          this.change_bg_zone()
        } else {
          alert(resp.data.message)
        }
      }
      this.saving = false;
      this.display = true;
      //this.$toasted.clear()
    },
    newDistribution() {
      // agrega un nuevo elemento a la lista distributions
      this.form.distributions.push({
        id: 0,
        percentage: 0
      }
      )
    },
    async removeDistibition(id_dist) {
      // remueve un elemento distribution por su id 
      const params = {
        id: id_dist
      };

      let resp = await axios.post('/api/zones/remove_dist/', params);
      if(resp.data.success){
        this.form.distributions = this.form.distributions.filter(f => f.id != id_dist)
        this.change_bg_zone()
      }else{
        alert(resp.data.message)
      }
    },
    formValidations() {
      
      let form_ok = true;
      let msg = ''
      // si esta vacio el nombre se agrega mensaje y se pone la bandera en false
      if (this.form.name.length == 0) {
        msg = "The zone name cannot be empty.\n";
        form_ok = false;
      }
      // se suman porcentajes
      let total = 0
      this.form.distributions.map((m) => total += parseInt(m.percentage))
      // si es mayor a 100 se agrega mensaje y se pone bandera en false
      if (total != 100) {
        msg += "The sum of all distributions must be ensured to be 100% in anyway.\n";
        form_ok = false;
      }

      // si la bandera es false esq que hay mensajes de error y se muestran
      if (!form_ok)
        alert(msg)
      // regresa bandera
      return form_ok
    },
    filterKey_number(e) {
      // Si el código es menor que 48 (0) o mayor que 57 (9)
      if ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode != 8 && e.keyCode != 46)) {
        // No se agrega
        e.preventDefault();
      }
    },
    filterKey_space(e) {
      // Se quitan dobles espacios mientras escribe
      this.form.name = this.form.name.replace(/\s+/, ' ')
      this.form.name = this.form.name.replace(/\s+/gi, ' ')
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.zone-editable {
  border: 1px solid $gray-color;
  padding: $qmb;
  border-radius: $border-radius;

  .zone-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .zone-edit {
    display: flex;
    flex-direction: column;
    gap: $small-action-space;

    .zone-edit-actions {
      display: flex;
      gap: $small-action-space;
      justify-content: end;
    }

    .zone-edit-distributions {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: $small-action-space;
    }
  }
}
</style>
