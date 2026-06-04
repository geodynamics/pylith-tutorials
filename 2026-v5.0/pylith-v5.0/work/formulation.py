"""
1. Strong form -> Weak form
2. PETSc formulation -> PETSc weak form
3. Elasticity boundary value problem -> add fault to boundary value problem
4. Elasticity w/fault: strong form -> weak form -> divergence theorem -> identify terms
"""
import manim

TEXT_FONT = "sans-serif"
TEXT_COLOR = manim.YELLOW
TEXT_SCALE = 0.5

TEX_FONT_SIZE = 32
TITLE_FONT_SIZE = 36

PDE_COLOR = manim.PURE_GREEN
PDE_COLOR2 = manim.BLUE_C
F0_COLOR = manim.TEAL_D
F1_COLOR = manim.PURPLE_C


def show_title(title, scene):
    scene.clear()
    scene.play(
        manim.FadeIn(title),
        run_time=2.0,
    )
    scene.wait(1.0)
    scene.play(
        manim.FadeOut(title),
        run_time=2.0,
    )


class FiniteElementFormulation:
    """General finite-element formulation: strong form to weak form."""

    def __init__(self):
        self.title = manim.Text(
            "Finite-Element Formulation for ODEs and PDEs", font=TEXT_FONT, font_size=TITLE_FONT_SIZE,
        )

        self.strong_text = manim.Text(
            "Given a partial differential equation (strong form)",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.strong_form = manim.MathTex(
            r"\vec{f}_0(t, s, \dot{s})",
            r"= \vec{0}",
            font_size=TEX_FONT_SIZE,
        )

        self.weak_text = manim.Paragraph(
            "We create the weak form by multiplying by a trial function",
            "and integrating over the domain",
            line_spacing=1.0,
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.weak_form = manim.MathTex(
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial} \cdot",
            r"\vec{f}_0(t, s, \dot{s})",
            r"\,d\Omega",
            r"= 0",
            font_size=TEX_FONT_SIZE,
        )
        self.weak_form[2].set_color(PDE_COLOR)
        self.weak_form[4].set_color(PDE_COLOR)

        manim.VGroup(
            self.strong_text,
            self.strong_form,
            self.weak_text,
            self.weak_form,
        ).arrange(manim.DOWN)
        self.strong_text.to_edge(manim.LEFT)
        self.weak_text.to_edge(manim.LEFT)

    @staticmethod
    def construct(scene):
        fe_formulation = FiniteElementFormulation()

        show_title(fe_formulation.title, scene)

        # Strong form
        scene.play(
            manim.Create(fe_formulation.strong_text),
            run_time=2.0,
        )
        scene.play(
            manim.Create(fe_formulation.strong_form),
            run_time=2.0,
        )
        scene.wait(2.0)

        # Weak form
        scene.play(
            manim.TransformFromCopy(
                fe_formulation.strong_form[0], fe_formulation.weak_form[2]
            ),
            run_time=2.0,
        )
        # Multiply by trial function
        scene.play(
            manim.Create(fe_formulation.weak_text[0]),
            run_time=2.0,
        )
        scene.play(
            manim.Create(fe_formulation.weak_form[1]),
            run_time=2.0,
        )
        scene.wait(1.0)
        # Integrate over domain
        scene.play(
            manim.Create(fe_formulation.weak_text[1]),
            run_time=2.0,
        )
        scene.play(
            manim.FadeIn(fe_formulation.weak_form[0]),
            manim.FadeIn(fe_formulation.weak_form[3]),
        )
        # Copy zeros
        scene.play(
            manim.TransformFromCopy(
                fe_formulation.strong_form[1], fe_formulation.weak_form[4]
            ),
            run_time=2.0,
        )
        scene.wait(2.0)


class PETScFormulation:
    """PETSc solver formulation."""

    def __init__(self):
        self.title = manim.Text(
            "PETSc Solver Formulation",
            font=TEXT_FONT,
            font_size=TITLE_FONT_SIZE,
        )

        self.general_text = manim.Text(
            "PETSc is designed to solve",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.general_form = manim.MathTex(
            r"F(t, s, \dot{s})",
            r"&=",
            r"G(t, s)",
            r"\\",
            r"s(t_0)",
            r"&=",
            r"s_o",
            font_size=TEX_FONT_SIZE,
        )

        self.fe_text = manim.Paragraph(
            "In using the finite-element method to solve partial differential equations",
            "we can often write the weak form as",
            line_spacing=1.0,
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.fe_form = manim.MathTex(
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial} \cdot",
            r"\vec{f}_0(t, s, \dot{s})",
            r"+",
            r"\nabla\vec{\psi}_\mathit{trial} :",
            r"\mathbf{f}_1(t, s, \dot{s})",
            r"\,d\Omega",
            r"=",
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial} \cdot",
            r"\vec{g}_0(t, s)",
            r"+",
            r"\nabla\vec{\psi}_\mathit{trial} :",
            r"\mathbf{g}_1(t, s)",
            r"\,d\Omega",
            font_size=TEX_FONT_SIZE,
        )
        self.fe_form[2].set_color(F0_COLOR)
        self.fe_form[5].set_color(F1_COLOR)
        self.fe_form[10].set_color(F0_COLOR)
        self.fe_form[13].set_color(F1_COLOR)

        manim.VGroup(
            self.general_text,
            self.general_form,
            self.fe_text,
            self.fe_form,
        ).arrange(manim.DOWN)
        self.general_text.to_edge(manim.LEFT)
        self.fe_text.to_edge(manim.LEFT)

        self.jacobian_text = manim.Paragraph(
            "To solve the system of equations, we must also compute the Jacobian",
            line_spacing=1.0,
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.jacobian_form = manim.MathTex(
            r"J_F &= ",
            r"\frac{\partial F}{\partial s}",
            r"+",
            r"s_\mathit{tshift} \frac{\partial F}{\partial \dot{s}}",
            r"\\",
            r"J_G &= ",
            r"\frac{\partial G}{\partial s}",
            font_size=TEX_FONT_SIZE,
        )

        manim.VGroup(
            self.general_text,
            self.general_form,
            self.jacobian_text,
            self.jacobian_form,
        ).arrange(manim.DOWN)
        self.general_text.to_edge(manim.LEFT)
        self.jacobian_text.to_edge(manim.LEFT)

    @staticmethod
    def construct(scene):
        petsc_formulation = PETScFormulation()

        show_title(petsc_formulation.title, scene)

        scene.play(
            manim.Create(petsc_formulation.general_text),
            run_time=2.0,
        )
        scene.play(
            manim.Create(petsc_formulation.general_form),
            run_time=2.0,
        )
        scene.wait(1.0)

        scene.play(
            manim.Create(petsc_formulation.fe_text),
            run_time=4.0,
        )
        scene.play(
            manim.TransformFromCopy(
                petsc_formulation.general_form[0], petsc_formulation.fe_form[:7]
            ),
            manim.TransformFromCopy(
                petsc_formulation.general_form[1], petsc_formulation.fe_form[7]
            ),
            manim.TransformFromCopy(
                petsc_formulation.general_form[2], petsc_formulation.fe_form[8:]
            ),
            run_time=2.0,
        )
        scene.wait(5.0)

        # Jacobian
        scene.play(
            manim.FadeOut(petsc_formulation.fe_text, petsc_formulation.fe_form),
        )
        scene.play(
            manim.Create(petsc_formulation.jacobian_text),
            run_time=2.0,
        )
        scene.play(
            manim.Create(petsc_formulation.jacobian_form),
            run_time=3.0,
        )
        scene.wait(5.0)


class ElasticityBVP:
    """Elasticity boundary value problem."""

    def __init__(self):
        self.title = manim.Text(
            "Elasticity Boundary Value Problem",
            font=TEXT_FONT,
            font_size=TITLE_FONT_SIZE,
        )

        self.elasticity_text = manim.Text(
            "Quasi-static elasticity boundary value problem",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.elasticity_bvp = manim.MathTex(
            r"\vec{f}(t, \vec{x}) + \nabla \sigma(\vec{u}) = \vec{0} \text{ in } \Omega \\",
            r"\sigma \cdot \vec{n} = \vec{\tau}(t, \vec{x}) \text{ on } \Gamma_\tau \\",
            r"\vec{u} = \vec{u}_0(t, \vec{x}) \text{ on } \Gamma_u \\",
            font_size=TEX_FONT_SIZE,
        )

        self.fault_text = manim.Text(
            "Add prescribed fault slip with equal and opposite tractions across fault",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.fault_bvp = manim.MathTex(
            r"\vec{u}^+ - \vec{u}^- - \vec{d}(t, \vec{x}) = \vec{0} \text{ on } \Gamma_f \\",
            r"\sigma \cdot \vec{n} = +\vec{\lambda} \text{ on } \Gamma_{f^+} \\",
            r"\sigma \cdot \vec{n} = -\vec{\lambda} \text{ on } \Gamma_{f^-} \\",
            font_size=TEX_FONT_SIZE,
        )

        manim.VGroup(
            self.elasticity_text,
            self.elasticity_bvp,
            self.fault_text,
            self.fault_bvp,
        ).arrange(manim.DOWN)
        self.elasticity_text.to_edge(manim.LEFT)
        self.fault_text.to_edge(manim.LEFT)

    @staticmethod
    def construct(scene):
        elasticity_bvp = ElasticityBVP()

        show_title(elasticity_bvp.title, scene)

        scene.play(
            manim.Create(elasticity_bvp.elasticity_text),
            run_time=2.0,
        )
        scene.play(
            manim.Create(elasticity_bvp.elasticity_bvp),
            run_time=8.0,
        )
        scene.wait(3.0)

        scene.play(
            manim.Create(elasticity_bvp.fault_text),
            run_time=4.0,
        )
        scene.play(
            manim.Create(elasticity_bvp.fault_bvp),
            run_time=6.0,
        )
        scene.wait(5.0)


class ElasticityFormulation:
    """Elasticity formulation."""

    def __init__(self):
        self.title = manim.Text(
            "Elasticity Finite-Element Formulation",
            font=TEXT_FONT,
            font_size=TITLE_FONT_SIZE,
        )

        self.strong_text = manim.Paragraph(
            "Start with quasi-static elasticity boundary value problem",
            "Include prescribed slip constraint equation",
            line_spacing=1.0,
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.strong_form = manim.MathTex(
            r"\vec{f}(t, \vec{x})",
            r"+",
            r"\nabla \cdot \sigma(\vec{u})",
            r"=",
            r"\vec{0}",
            r"\text{ in } \Omega",
            r"\\",
            r"\vec{u}^+ - \vec{u}^- - \vec{d}(t, \vec{x})",
            r"=",
            r"\vec{0}",
            r"\text{ on } \Gamma_f",
            font_size=TEX_FONT_SIZE,
        )
        self.strong_form_parts = {
            "elasticity": self.strong_form[:6],
            "fault": self.strong_form[7:],
            "elasticity_pde": self.strong_form[0:3],
            "elasticity_0": self.strong_form[3:5],
            "fault_pde": self.strong_form[7],
            "slip_0": self.strong_form[8:10],
        }
        self.strong_form_parts["elasticity_pde"].set_color(PDE_COLOR)
        self.strong_form_parts["fault_pde"].set_color(PDE_COLOR2)

        self.weak_text = manim.Paragraph(
            "We create the weak form by multiplying by trial functions",
            "and integrating over the domain",
            line_spacing=1.0,
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.weak_form = manim.MathTex(
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\left(",
            r"\vec{f}(t, \vec{x})",
            r"+",
            r"\nabla \cdot \sigma(\vec{u})",
            r"\right)",
            r"\,d\Omega",
            r"=",
            r"0",
            r"\\",
            r"\int_{\Gamma_f}",
            r"\vec{\psi}_\mathit{trial}^\lambda \cdot",
            r" \left( \vec{u}^+ - \vec{u}^- - \vec{d}(t, \vec{x}) \right)",
            r"\,d\Gamma",
            r"=",
            r"0",
            font_size=TEX_FONT_SIZE,
        )
        self.weak_form[2:7].set_color(PDE_COLOR)
        self.weak_form[13].set_color(PDE_COLOR2)
        self.weak_form_parts = {
            "elasticity_pde": self.weak_form[2:7],
            "elasticity_trial": self.weak_form[1],
            "elasticity_integral": manim.VGroup(
                self.weak_form[0],
                self.weak_form[7],
            ),
            "elasticity_0": self.weak_form[8:10],
            "fault_pde": self.weak_form[13],
            "fault_trial": self.weak_form[12],
            "fault_integral": manim.VGroup(
                self.weak_form[11],
                self.weak_form[14],
            ),
            "slip_0": self.weak_form[15:],
            "body_force": self.weak_form[3],
            "stress": self.weak_form[5],
            "slip": self.weak_form[13],
        }

        manim.VGroup(
            self.strong_text,
            self.strong_form,
            self.weak_text,
            self.weak_form,
        ).arrange(manim.DOWN)
        self.strong_text.to_edge(manim.LEFT)
        self.weak_text.to_edge(manim.LEFT)

        self.divergence_text = manim.Text(
            "Using the divergence theorem, we can write",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.divergence_result = manim.MathTex(
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\left( \nabla \cdot \sigma(\vec{u}) \right)",
            r"\,d\Omega",
            r"=",
            r"\int_\Omega",  # 5
            r"\nabla \vec{\psi}_\mathit{trial}^u :",
            r"(-\sigma(\vec{u})",
            r"\,d\Omega",
            r"+",
            r"\int_\Gamma",  # 10
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\left( \sigma(\vec{u}) \cdot \vec{n} \right)",
            r"\,d\Gamma",
            font_size=TEX_FONT_SIZE,
        )
        self.divergence_result_parts = {
            "divergence_stress": self.divergence_result[0:4],
            "inner_product": self.divergence_result[5:9],
            "traction": self.divergence_result[10:],
        }

        self.residual_text = manim.Text(
            "Substituting into the weak form, we have",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.residual_result = manim.MathTex(
            r"\int_\Omega",  # 0
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\vec{f}(t, \vec{x})",
            r"\,d\Omega",
            r"+",
            r"&\int_\Omega",  # 5
            r"\nabla \vec{\psi}_\mathit{trial}^u :",
            r"(-\sigma(\vec{u}))",
            r"\,d\Omega",
            r"+",
            r"\int_{\Gamma_\tau}",  # 10
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\vec{\tau}(t,\vec{x})",
            r"\,d\Gamma",
            r"\\",
            r"+",
            r"&\int_{\Gamma_{f^+}}",  # 16
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\vec{\lambda}(t,\vec{x})",
            r"\,d\Gamma",
            r"+",
            r"\int_{\Gamma_{f^-}}",  # 21
            r"\vec{\psi}_\mathit{trial}^u \cdot",
            r"\vec{-\lambda}(t,\vec{x})",
            r"\,d\Gamma",
            r"=",  # 25
            r"0",
            r"\\[12pt]",
            r"&\int_{\Gamma_f}",  # 28
            r"\vec{\psi}_\mathit{trial}^\lambda \cdot",
            r" \left( \vec{u}^+ - \vec{u}^- - \vec{d}(t, \vec{x}) \right)",
            r"\,d\Gamma",
            r"=",  # 32
            r"0",
            font_size=TEX_FONT_SIZE,
        )
        self.residual_result[2].set_color(PDE_COLOR)
        self.residual_result[7].set_color(PDE_COLOR)
        self.residual_result[12].set_color(PDE_COLOR)
        self.residual_result[18].set_color(PDE_COLOR)
        self.residual_result[23].set_color(PDE_COLOR)
        self.residual_result[30].set_color(PDE_COLOR2)
        self.residual_result_parts = {
            "body_force_integral": self.residual_result[0:4],
            "stress_integral": self.residual_result[4:9],
            "traction_integral": self.residual_result[9:14],
            "faultpos_integral": self.residual_result[15:20],
            "faultneg_integral": self.residual_result[20:25],
            "elasticity_0": self.residual_result[25:27],
            "slip_integral": self.residual_result[28:32],
            "slip_0": self.residual_result[32:],
        }

        self.weak_form_top = self.weak_form.copy()
        self.weak_form_top.to_edge(manim.UP)
        manim.VGroup(
            self.weak_form_top,
            self.divergence_text,
            self.divergence_result,
            self.residual_text,
            self.residual_result,
        ).arrange(manim.DOWN)
        self.divergence_text.to_edge(manim.LEFT)
        self.residual_text.to_edge(manim.LEFT)

        self.petsc_form_text = manim.Text(
            "Recall that we use PETSc to solve equations of the form",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.petsc_form = manim.MathTex(
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial} \cdot",
            r"\vec{f}_0(t, s, \dot{s})",
            r"+",
            r"\nabla\vec{\psi}_\mathit{trial} :",
            r"\mathbf{f}_1(t, s, \dot{s})",
            r"\,d\Omega",
            r"=",
            r"\int_\Omega",
            r"\vec{\psi}_\mathit{trial} \cdot",
            r"\vec{g}_0(t, s)",
            r"+",
            r"\nabla\vec{\psi}_\mathit{trial} :",
            r"\mathbf{g}_1(t, s)",
            r"\,d\Omega",
            font_size=TEX_FONT_SIZE,
        )
        self.petsc_form[2].set_color(F0_COLOR)
        self.petsc_form[5].set_color(F1_COLOR)
        self.petsc_form[10].set_color(F0_COLOR)
        self.petsc_form[13].set_color(F1_COLOR)

        self.residual_terms_text = manim.MarkupText(
            "Identifying f<sub>0</sub>, f<sub>1</sub>, g<sub>0</sub> and g<sub>1</sub>, we have",
            color=TEXT_COLOR,
            font=TEXT_FONT,
        ).scale(TEXT_SCALE)

        self.residual_terms_disp = manim.MathTex(
            r"\int_\Omega {\vec{\psi}_\mathit{trial}^{u}} \cdot ",
            r"\underbrace{\vec{f}(\vec{x},t)}_{\vec{f}^u_0}", # 1
            r"&+ \nabla {\vec{\psi}_\mathit{trial}^{u}} : ",
            r"\underbrace{-\boldsymbol{\sigma}(\vec{u})}_{\boldsymbol{f^u_1}}", # 3
            r"\, d\Omega",
            r"+ \int_{\Gamma_\tau} {\vec{\psi}_\mathit{trial}^{u}} \cdot",
            r"\underbrace{\vec{\tau}(\vec{x},t)}_{\vec{f}^u_0}", # 6
            r"\, d\Gamma",
            r"\\",
            r"&+ \int_{\Gamma_{f}} {",
            r"\vec{\psi}_\mathit{trial}^{u^+}} \cdot",
            r"\underbrace{\left(-\vec{\lambda}(\vec{x},t)\right)}_{\vec{f}^u_0}", # 11
            r" + {\vec{\psi}_\mathit{trial}^{u^-}} \cdot",
            r"\underbrace{\left(+\vec{\lambda}(\vec{x},t)\right)}_{\vec{f}^u_0}", # 13
            r"\, d\Gamma",
            r"= 0",
            font_size=TEX_FONT_SIZE,
        )
        self.residual_terms_disp[1].set_color(F0_COLOR)
        self.residual_terms_disp[3].set_color(F1_COLOR)
        self.residual_terms_disp[6].set_color(F0_COLOR)
        self.residual_terms_disp[11].set_color(F0_COLOR)
        self.residual_terms_disp[13].set_color(F0_COLOR)

        self.residual_terms_lagrange = manim.MathTex(
            r"\int_{\Gamma_{f}} {\vec{\psi}_\mathit{trial}^{\lambda}} \cdot",
            r"\underbrace{\left(-\vec{u}^+ + \vec{u}^- + \vec{d}(\vec{x},t) \right)}_{\vec{f}^\lambda_0}",
            r"\, d\Gamma",
            r"= 0",
            font_size=TEX_FONT_SIZE,
        )
        self.residual_terms_lagrange[1].set_color(F0_COLOR)

        self.weak_form_top.to_edge(manim.UP)
        manim.VGroup(
            self.petsc_form_text,
            self.petsc_form,
            self.residual_terms_text,
            self.residual_terms_disp,
            self.residual_terms_lagrange,
        ).arrange(manim.DOWN)
        self.petsc_form_text.to_edge(manim.LEFT)
        self.residual_terms_text.to_edge(manim.LEFT)

    @staticmethod
    def construct(scene):
        formulation = ElasticityFormulation()

        show_title(formulation.title, scene)

        # Strong form: elasticity
        scene.play(
            manim.Succession(
                manim.Create(formulation.strong_text[0]),
                manim.Create(formulation.strong_form_parts["elasticity"]),
            ),
            run_time=4.0,
        )
        scene.wait(2.0)

        # Strong form: fault
        scene.play(
            manim.Succession(
                manim.Create(formulation.strong_text[1]),
                manim.Create(formulation.strong_form_parts["fault"]),
            ),
            run_time=4.0,
        )
        scene.wait(4.0)

        # Weak form
        scene.play(
            manim.Indicate(formulation.strong_form_parts["elasticity_pde"]),
            manim.Indicate(formulation.strong_form_parts["fault_pde"]),
        )
        scene.play(
            manim.TransformFromCopy(
                formulation.strong_form_parts["elasticity_pde"],
                formulation.weak_form_parts["elasticity_pde"],
            ),
            manim.TransformFromCopy(
                formulation.strong_form_parts["fault_pde"],
                formulation.weak_form_parts["fault_pde"],
            ),
        )
        # Multiply by trial function
        scene.play(
            manim.Succession(
                manim.Create(formulation.weak_text[0]),
                manim.Create(formulation.weak_form_parts["elasticity_trial"]),
                manim.Create(formulation.weak_form_parts["fault_trial"]),
            ),
            run_time=4.0,
        )
        # Integrate over domain
        scene.play(
            manim.Succession(
                manim.Create(formulation.weak_text[1]),
                manim.Create(formulation.weak_form_parts["elasticity_integral"]),
                manim.Create(formulation.weak_form_parts["fault_integral"]),
            ),
            run_time=3.0,
        )
        # Set integral to zero
        scene.play(
            manim.TransformFromCopy(
                formulation.strong_form_parts["elasticity_0"],
                formulation.weak_form_parts["elasticity_0"],
            ),
            manim.TransformFromCopy(
                formulation.strong_form_parts["slip_0"],
                formulation.weak_form_parts["slip_0"],
            ),
        )
        scene.wait(5.0)

        # Move weak form up
        scene.play(
            manim.FadeOut(
                formulation.strong_text,
                formulation.strong_form,
                formulation.weak_text,
            ),
            run_time=1.0,
        )
        scene.play(
            manim.ReplacementTransform(
                formulation.weak_form, formulation.weak_form_top
            ),
        )
        scene.play(
                manim.Create(formulation.divergence_text),
            run_time=2.5,
        )

        # Divergence theorem
        scene.play(
            manim.Indicate(formulation.weak_form_parts["stress"]),
        )
        scene.remove(formulation.weak_form_parts["stress"])
        scene.play(
            manim.TransformFromCopy(
                formulation.weak_form_parts["stress"],
                formulation.divergence_result[2]
            ),
        )
        scene.play(
            manim.Succession(
                manim.Create(formulation.divergence_result[0:2]),
                manim.Create(formulation.divergence_result[3:]),
            ),
            run_time=4.0,
        )
        scene.wait(5.0)

        # Residual after using divergence theorem
        scene.play(
            manim.Succession(
                manim.Create(formulation.residual_text),
            ),
            run_time=2.0,
        )
        scene.play(
            manim.TransformFromCopy(
                formulation.weak_form_parts["body_force"],
                formulation.residual_result_parts["body_force_integral"],
            ),
        )
        scene.wait(1.0)
        scene.play(
            manim.TransformFromCopy(
                formulation.divergence_result_parts["inner_product"],
                formulation.residual_result_parts["stress_integral"],
            ),
        )
        scene.wait(1.0)
        scene.play(
            manim.TransformFromCopy(
                formulation.divergence_result_parts["traction"],
                formulation.residual_result_parts["traction_integral"],
            ),
        )
        scene.wait(1.0)
        scene.play(
            manim.TransformFromCopy(
                formulation.divergence_result_parts["traction"],
                formulation.residual_result_parts["faultpos_integral"],
            ),
            manim.TransformFromCopy(
                formulation.divergence_result_parts["traction"],
                formulation.residual_result_parts["faultneg_integral"],
            ),
        )
        scene.wait(1.0)
        scene.play(
            manim.TransformFromCopy(
                formulation.weak_form_parts["elasticity_0"],
                formulation.residual_result_parts["elasticity_0"],
            ),
        )
        scene.wait(1.0)
        scene.play(
            manim.TransformFromCopy(
                formulation.weak_form_parts["slip"],
                formulation.residual_result_parts["slip_integral"],
            ),
            manim.TransformFromCopy(
                formulation.weak_form_parts["slip_0"],
                formulation.residual_result_parts["slip_0"],
            ),
        )
        scene.wait(5.0)

        # Residual terms
        scene.play(
            manim.FadeOut(
                formulation.weak_form_top,
                formulation.divergence_text,
                formulation.divergence_result,
                formulation.residual_text,
                formulation.residual_result,
            ),
        )
        scene.play(
            manim.Succession(
                manim.Create(formulation.petsc_form_text),
                manim.Create(formulation.petsc_form),
            ),
            run_time=4.0,
        )
        scene.play(
            manim.Succession(
                manim.Create(formulation.residual_terms_text),
                manim.Create(formulation.residual_terms_disp),
                manim.Create(formulation.residual_terms_lagrange),
            ),
            run_time=12.0,
        )
        scene.wait(5.0)


class Animation(manim.Scene):
    def construct(self):
        FiniteElementFormulation.construct(self)
        PETScFormulation.construct(self)
        ElasticityBVP.construct(self)
        ElasticityFormulation.construct(self)
