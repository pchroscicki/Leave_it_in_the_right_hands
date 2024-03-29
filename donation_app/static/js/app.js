document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          // STOP movement if form is not valid
          if (this.validateForm() === false) return false;
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Form validation - empty fields
     */
    validateForm() {
      // Initial data
      let step = document.querySelectorAll('.step')[this.currentStep-1]
      let inputs = step.querySelectorAll('input');
      let valid_inputs = 0;
      let valid = true;

      // Check if category input is empty:
      for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === 'checkbox' && inputs[i].checked) {
          valid_inputs++;
        } if (inputs[i].type === 'radio' && inputs[i].checked) {
          valid_inputs++;
        } else {
          if (inputs[i].value === '' || inputs[i].value === null) {
            valid_inputs--;
          }
        }
      }

      // Defines an adequate alert to display and returns 'false' value
      if (this.currentStep === 1 && valid_inputs === 0) {
        alert ('Zaznacz kategorię darów do przekazania');
        valid = false;
      }
      if (this.currentStep === 2 && valid_inputs < 0) {
        alert('Podaj łączną liczbę worków do przekazania');
        valid = false;
      }
      if (this.currentStep === 2 && inputs[0].value < 1) {
        alert('Minimalna liczba worków do przekazania to 1 szt.');
        valid = false;
      }
      if (this.currentStep === 3 && valid_inputs === 0) {
        alert('Wybierz organizację, którą chcesz wesprzeć');
        valid = false;
      }
      if (this.currentStep === 4 && valid_inputs < 0) {
        alert('Uzupełnij wszytskie pola dotyczące miejsca, daty i czasu odbioru');
        valid = false;
      }
      return valid;
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;
      var category_form = document.getElementById("category-form");
      var institution_form = document.getElementById("institution-form");
      var address_form = document.getElementById("address-form");
      var data_form = document.getElementById("data-form");
      var selected_categories = Array.from(category_form.querySelectorAll("input[name='categories']:checked"));

      // institutions screening (narrows down the institution list to those that accept selected items)
      if (this.currentStep === 2) {
          var institutions = Array.from(institution_form.querySelectorAll(".single_institute"));
          for (var i = 0; i < institutions.length; i++) {
            let categories_institution = Array.from(institutions[i].dataset.categories.replace(/\D/g, ""));
            var category_match = 0;
            for (var j = 0; j < selected_categories.length; j++) {
              if (categories_institution.includes(selected_categories[j].value)) {
                category_match++}
              }
            if (category_match !== selected_categories.length) {institutions[i].style.display = 'none'}
          }
        }

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // donation summary
      if (this.currentStep === 5) {
        var bags = document.getElementById("bags").value;
        var bags_content = [];
        for (var k = 0; k < selected_categories.length; k++) {
          var category_name = selected_categories[k].dataset.name;
          bags_content.push(category_name);
        }
        var bags_content_str = bags_content.join(', ');
        var summary = document.querySelector('.summary');
        summary.querySelector('#sum_bags').innerText = 'Worki: '+bags+' szt. z: '+bags_content_str+''
        var institution = (institution_form.querySelector("input[name='organization']:checked")).dataset.name;
        summary.querySelector('#sum_institution').innerText = 'Dla '+institution+'';

        // address summary
        summary.querySelector('#address').innerText = (address_form.querySelector("input[name='address']")).value;
        summary.querySelector('#city').innerText = (address_form.querySelector("input[name='city']")).value;
        summary.querySelector('#postcode').innerText = (address_form.querySelector("input[name='postcode']")).value;
        summary.querySelector('#phone').innerText = (address_form.querySelector("input[name='phone']")).value;

        // data info
        summary.querySelector('#data').innerText = (data_form.querySelector("input[name='data']")).value;
        summary.querySelector('#time').innerText = (data_form.querySelector("input[name='time']")).value
        summary.querySelector('#info').innerText = (data_form.querySelector("textarea[name='more_info']")).value;
      }
    }

    /**
     * Submit form
     */
    submit() {
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});