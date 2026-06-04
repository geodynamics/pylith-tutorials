"""
See mesh_quad.svg for a diagram of the mesh.

1. Create domain; add fault.
2. Mark fault (edges/faces); show edge orientation.
3. Orient fault (edges/faces); update edge orientation.
4. Create label with fault code (on fault, touches fault, doesn't touch fault; side of fault)
5. Create label with transform code (identity, split, unsplit, impinging; side of fault)
6. Transform topology and create coordinates for new entities.
8. Create new SF.
"""
import manim
import numpy

DOMAIN_X = 12.0
DOMAIN_Y = 6.0
FAULT_X = 3.0
FONT = "sans-serif"
TITLE_SCALE = 0.5
FAULT_LINEWIDTH = 6


def create_title(title: str):
    title = manim.Text(title, font=FONT).scale(TITLE_SCALE)
    title.to_edge(manim.UL)
    return title

class Domain:
    """Filled rectangular domain with fault.
    """
    DOMAIN_COLOR = manim.YELLOW_E
    FAULT_COLOR = manim.YELLOW_C

    def __init__(self):
        self.title = create_title("1. Mesh generator: Create domain geometry")
        self.rectangle = manim.Rectangle(width=DOMAIN_X, height=DOMAIN_Y)
        self.rectangle.set_fill(self.DOMAIN_COLOR, opacity=0.6)
        self.fault = manim.Line(start=(-FAULT_X, 0, 0), end=(+FAULT_X, 0, 0), stroke_width=FAULT_LINEWIDTH, color=self.FAULT_COLOR)

    def display(self, scene):
        scene.play(
            manim.FadeIn(self.title),
        )
        scene.play(
            manim.Create(self.rectangle),
            run_time=1.5,
        )
        scene.play(
            manim.Create(self.fault),
            run_time=1.5,
        )


class Mesh:
    """Finite-element mesh transformation.
    """
    NUM_X = 8
    NUM_Y = 5
    DX = 1.5
    COHESIVE_OFFSET = 0.1
    EXPLODE_FAULT = False

    COLOR_VERTEX = manim.WHITE
    COLOR_CELL = manim.GRAY_C
    COLOR_EDGE = manim.GRAY_B
    COLOR_EDGE_FAULT = manim.YELLOW_A
    COLOR_CELL_FAULT = manim.YELLOW_C
    CELL_OPACITY = 0.5

    COLOR_IMPINGING_NEG = manim.BLUE_C
    COLOR_TOUCHING_NEG = manim.BLUE_E
    COLOR_SPLIT_NEG = manim.BLUE_B
    COLOR_UNSPLIT_NEG = manim.BLUE_E
    COLOR_IMPINGING_POS = manim.RED_C
    COLOR_TOUCHING_POS = manim.RED_E
    COLOR_SPLIT_POS = manim.RED_B
    COLOR_UNSPLIT_POS = manim.RED_E

    CELLS_HIDE = (
        16, 17, 22, 23
    )
    EDGES_HIDE = (
        50, 55, 85, 90,
    )
    VERTICES_HIDE = (
        18, 19, 20, 24, 25, 26
    )
    EDGES_HIDE_ORIG = (
        16, 17, 18, 19, 20, 21, 22, 23
    )

    EDGES_FAULT = (
        26, 27, 28, 29        
    )
    VERTEX_FAULT_NEG = (
        29, 30, 31, 32, 33,
    )

    CELLS_COHESIVE = (
        18, 19, 20, 21,
    )
    EDGES_COHESIVE = (
        60, 65, 70, 75, 80,
    )
    EDGES_NEW_TOUCHING_POS = (
        17, 22,
    )
    VERTICES_NEW = (
        21, 22, 23,
    )

    CELLS_IMPINGING_POS = (
        10, 11, 12, 13,
    )
    CELLS_IMPINGING_NEG = (
        26, 27, 28, 29,
    )
    EDGES_IMPINGING_POS = (
        18, 19, 20, 21,
    )
    EDGES_IMPINGING_NEG = (
        26, 27, 28, 29,
    )

    CELLS_TOUCHING_POS = (
        9, 14,
    )
    CELLS_TOUCHING_NEG = (
        25, 30,
    )
    EDGES_TOUCHING_POS = (
        17, 59, 64, 69, 74, 79, 22,
    )
    EDGES_TOUCHING_NEG = (
        25, 61, 66, 71, 76, 81, 30,
    )

    VERTICES_SPLIT_NEG = (
        30, 31, 32,
    )
    VERTICES_UNSPLIT_NEG = (
        29, 33,
    )

    def __init__(self):
        self.titles = (
            create_title("2. Mesh generator: Discretize domain"),
            create_title("3. Mesh generator: Mark fault"),
            create_title("4. PyLith: Orient fault"),
            create_title("5. PyLith: Label fault entities"),
            create_title("6. PyLith: Set transform operations"),
            create_title("7. PyLith: Transform topology and set coordinates of new entities"),
            create_title("8. PyLith: Update interprocessor communication"),
        )

        self.vertices = self._create_vertices()
        self.cells = self._create_cells()
        self.edges = self._create_edges()
        self.i_step = 0

    def discretize(self, scene: manim.Scene):
        scene.play(
            manim.FadeOut(scene.domain.title),
        )
        scene.play(
            manim.FadeIn(self.titles[self.i_step]),
        )

        geometry = manim.VGroup(*(self.vertices))
        scene.play(
            manim.Create(geometry),
            run_time=2.0,
        )
        geometry = manim.VGroup(*(self.edges+self.cells))
        scene.play(
            manim.Create(geometry),
            run_time=1.0,
        )
        scene.play(
            manim.FadeOut(scene.domain.rectangle, scene.domain.fault),
            run_time=0.5,
        )
        self.i_step += 1

    def mark_fault(self, scene: manim.Scene):
        self._update_title(scene)

        edges_marked = self._create_fault_edges()
        geometry_out = manim.Group(*(self.edges))
        geometry_in = manim.Group(*(edges_marked))
        scene.play(
            manim.FadeOut(geometry_out),
            manim.FadeIn(geometry_in),
            run_time=2.0,
        )
        self.edges = edges_marked
        self.i_step += 1

    def orient_fault(self, scene):
        self._update_title(scene)
        orientation_orig = self._create_orientation(oriented=False)
        orientation_new = self._create_orientation(oriented=True)
        geometry_out = manim.Group(*(orientation_orig))
        geometry_in = manim.Group(*(orientation_new))
        scene.play(
            manim.FadeIn(geometry_out),
            run_time=2.0,
        )
        scene.wait(1)
        scene.play(
            manim.FadeOut(geometry_out),
            manim.FadeIn(geometry_in),
            run_time=2.0,
        )
        scene.wait(2)
        scene.play(
            manim.FadeOut(geometry_in),
            run_time=2.0,
        )
        self.i_step += 1

    def label_fault_points(self, scene):
        self._update_title(scene)

        new_cells = self._label_fault_cells()
        new_edges = self._label_fault_edges()
        new_vertices = self._label_fault_vertices()
        geometry_out = manim.Group(*(self.cells + self.edges + self.vertices))
        geometry_in = manim.Group(*(new_cells + new_edges + new_vertices))
        scene.play(
            manim.FadeOut(geometry_out),
            manim.FadeIn(geometry_in),
            run_time=2.0,
        )
        self.cells = new_cells
        self.edges = new_edges
        self.vertices = new_vertices
        self.i_step += 1

    def set_transform_ops(self, scene):
        self._update_title(scene)
        #new_cells = self._label_fault_cells()
        #new_edges = self._label_fault_edges()
        new_vertices = self._label_topology_ops_vertices()
        geometry_out = manim.Group(*(self.vertices))
        geometry_in = manim.Group(*(new_vertices))
        scene.play(
            manim.FadeOut(geometry_out),
            manim.FadeIn(geometry_in),
            run_time=2.0,
        )
        #self.cells = new_cells
        #self.edges = new_edges
        self.vertices = new_vertices
        self.i_step += 1

    def transform_topology(self, scene):
        self._update_title(scene)
        new_cells = self._transform_cells()
        new_edges = self._transform_edges()
        new_vertices = self._transform_vertices()
        geometry_out = manim.Group(*(self.cells + self.edges + self.vertices))
        geometry_in = manim.Group(*(new_cells + new_edges + new_vertices))
        scene.add(geometry_in)
        scene.play(
            manim.FadeOut(geometry_out),
            manim.FadeIn(geometry_in),
            run_time=2.0,
        )
        self.cells = new_cells
        self.edges = new_edges
        self.vertices = new_vertices
        self.i_step += 1

    def update_petscsf(self, scene):
        self._update_title(scene)
        self.i_step += 1

    def _update_title(self, scene: manim.Scene):
        scene.play(
            manim.FadeOut(self.titles[self.i_step-1]),
        )
        scene.play(
            manim.FadeIn(self.titles[self.i_step]),
        )

    def _create_vertices(self):
        x1 = numpy.arange(-0.5*DOMAIN_X, +0.5*DOMAIN_X+0.1*self.DX, self.DX)
        if self.EXPLODE_FAULT:
            y1 = numpy.array([+3, +1.5, +self.COHESIVE_OFFSET, -self.COHESIVE_OFFSET, -1.5, -3.0])
        else:
            y1 = numpy.array([+3, +1.5, +0.0, -0.0, -1.5, -3.0])
        x, y = numpy.meshgrid(x1, y1, indexing="xy")
        vertices = numpy.stack( (x.ravel(), y.ravel()) ).T
        dots = [manim.Dot((x_point, y_point, 0.0), color=self.COLOR_VERTEX, z_index=2) for x_point, y_point in vertices]
        for index in self.VERTICES_HIDE + self.VERTICES_NEW:
            dots[index].set_opacity(0)
        return dots

    def _create_cells(self):
        indices0 = numpy.arange(0, self.NUM_X, 1, dtype=numpy.int32)
        indices1 = indices0 + self.NUM_X+1
        indices2 = indices1 + 1
        indices3 = indices0 + 1
        cells = []
        for i_y in range(self.NUM_Y):
            offset = i_y*(self.NUM_X+1)
            for i0, i1, i2, i3 in zip(indices0, indices1, indices2, indices3):
                cells.append([i0+offset, i1+offset, i2+offset, i3+offset])
        polygons = []
        for cell in cells:
            p0 = self.vertices[cell[0]].get_center()
            p1 = self.vertices[cell[1]].get_center()
            p2 = self.vertices[cell[2]].get_center()
            p3 = self.vertices[cell[3]].get_center()
            polygon = manim.Polygon(p0, p1, p2, p3, stroke_opacity=0, fill_color=self.COLOR_CELL, fill_opacity=self.CELL_OPACITY, z_index=0)
            polygons.append(polygon)

        for index in self.CELLS_HIDE + self.CELLS_COHESIVE:
            polygons[index].set_opacity(0)

        return polygons

    def _create_edges(self):
        edges = []
        # Edges in x direction
        indices0 = numpy.arange(0, self.NUM_X, 1, dtype=numpy.int32)
        indices1 = indices0 + 1
        for i_y in range(self.NUM_Y+1):
            offset = i_y*(self.NUM_X+1)
            for i0, i1 in zip(indices0, indices1):
                edges.append([i0+offset, i1+offset])

        # Edges in y direction
        indices0 = (self.NUM_X+1) * numpy.arange(0, self.NUM_Y, 1, dtype=numpy.int32)
        indices1 = indices0 + self.NUM_X+1
        for i_x in range(self.NUM_X+1):
            offset = i_x
            for i0, i1 in zip(indices0, indices1):
                edges.append([i0+offset, i1+offset])

        lines = []
        for edge in edges:
            p0 = self.vertices[edge[0]].get_center()
            p1 = self.vertices[edge[1]].get_center()
            line = manim.Line(p0, p1, color=self.COLOR_EDGE, z_index=1)
            lines.append(line)

        for index in self.EDGES_HIDE + self.EDGES_HIDE_ORIG + self.EDGES_COHESIVE:
            lines[index].set_opacity(0)

        return lines

    def _create_orientation(self, oriented: bool):
        arrows = []
        for i_x, x in enumerate(self.DX * numpy.arange(-1.5, +1.51, +1.0)):
            start, end = (manim.RIGHT, manim.LEFT) if i_x in [2] and not oriented else (manim.LEFT, manim.RIGHT)
            arrow = manim.Arrow(start=start, end=end, color=manim.WHITE, max_stroke_width_to_length_ratio=8, max_tip_length_to_length_ratio=0.2)
            arrow.move_to((x, self.COHESIVE_OFFSET, 0))
            arrow.set_length(1.0)
            arrows.append(arrow)

        return arrows

    def _create_fault_edges(self):
        edges = [edge.copy() for edge in self.edges]
        for index in self.EDGES_FAULT:
            edges[index].set(stroke_color=self.COLOR_CELL_FAULT, stroke_width=FAULT_LINEWIDTH)
        return edges

    def _label_fault_cells(self):
        cells = [cell.copy() for cell in self.cells]
        for index in self.CELLS_IMPINGING_NEG:
            cells[index].set(fill_color=self.COLOR_IMPINGING_NEG)
        for index in self.CELLS_IMPINGING_POS:
            cells[index].set(fill_color=self.COLOR_IMPINGING_POS)
        for index in self.CELLS_TOUCHING_NEG:
            cells[index].set(fill_color=self.COLOR_TOUCHING_NEG)
            cells[index].set_opacity(0.7*self.CELL_OPACITY)
        for index in self.CELLS_TOUCHING_POS:
            cells[index].set(fill_color=self.COLOR_TOUCHING_POS)
            cells[index].set_opacity(0.7*self.CELL_OPACITY)
        return cells

    def _label_fault_edges(self):
        edges = [edge.copy() for edge in self.edges]
        for index in self.EDGES_TOUCHING_NEG:
            edges[index].set(stroke_color=self.COLOR_TOUCHING_NEG)
        for index in self.EDGES_TOUCHING_POS:
            edges[index].set(stroke_color=self.COLOR_TOUCHING_POS)
        for index in self.EDGES_IMPINGING_NEG:
            edges[index].set(stroke_color=self.COLOR_IMPINGING_NEG)
        return edges

    def _label_fault_vertices(self):
        vertices = [vertex.copy() for vertex in self.vertices]
        for index in self.VERTEX_FAULT_NEG:
            vertices[index].set(color=self.COLOR_TOUCHING_NEG)
        return vertices

    def _label_topology_ops_vertices(self):
        vertices = [vertex.copy() for vertex in self.vertices]
        for index in self.VERTICES_SPLIT_NEG:
            vertices[index].set(color=self.COLOR_SPLIT_NEG)
        for index in self.VERTICES_UNSPLIT_NEG:
            vertices[index].set(color=self.COLOR_UNSPLIT_NEG)
        return vertices

    def _transform_points(self, points, offset):
        dx = self.DX
        mask_y = numpy.abs(points[:,1]) < 0.5*dx 
        mask_left = numpy.logical_and(points[:,0] >= -2*dx, points[:,0] < -dx)
        offset_left = (points[:,0] + 2*dx) * offset / dx

        mask_center = numpy.logical_and(points[:,0] >= -dx, points[:,0] < +dx)
        offset_center = offset

        mask_right = numpy.logical_and(points[:,0] >= +dx, points[:,0] < +2*dx)
        offset_right = (2*dx - points[:,0]) * offset / dx
        
        points[:,1] += mask_y * (mask_left*offset_left + mask_center*offset_center + mask_right*offset_right)

    def _transform_points_fault(self, points):
        dx = self.DX
        offset = self.COHESIVE_OFFSET
        mask_pos = numpy.array([
            True, True, False, False,
            False, False, False, False,
            False, False,  True,  True, 
            True,  True,  True,  True
            ])
        sign = mask_pos*1.0 - ~mask_pos*1.0
        mask_left = numpy.logical_and(points[:,0] >= -2*dx, points[:,0] < -dx)
        offset_left = (points[:,0] + 2*dx) * offset / dx

        mask_center = numpy.logical_and(points[:,0] >= -dx, points[:,0] < +dx)
        offset_center = offset

        mask_right = numpy.logical_and(points[:,0] >= +dx, points[:,0] < +2*dx)
        offset_right = (2*dx - points[:,0]) * offset / dx
        
        points[:,1] += sign * (mask_left*offset_left + mask_center*offset_center + mask_right*offset_right)

    def _transform_cells(self):
        cells = [cell.copy() for cell in self.cells]
        for cell in cells:
            cell.set(fill_color=self.COLOR_CELL)
            cell.set_opacity(self.CELL_OPACITY)
        for index in self.CELLS_COHESIVE:
            cell = cells[index]
            cell.set(stroke_color=self.COLOR_EDGE_FAULT, fill_color=self.COLOR_CELL_FAULT)
            cell.set_opacity(self.CELL_OPACITY)
            self._transform_points_fault(cell.points)
        for index in self.CELLS_IMPINGING_POS:
            cell = cells[index]
            self._transform_points(cell.points, offset=+self.COHESIVE_OFFSET)
        for index in self.CELLS_IMPINGING_NEG:
            cell = cells[index]
            self._transform_points(cell.points, offset=-self.COHESIVE_OFFSET)
        return cells

    def _transform_edges(self):
        edges = [edge.copy() for edge in self.edges]
        for edge in edges:
            edge.set(stroke_color=self.COLOR_EDGE)
        for index in self.EDGES_COHESIVE:
            edge = edges[index]
            edge.set(stroke_color=self.COLOR_EDGE_FAULT)
            edge.set_opacity(1)
        for index in self.EDGES_NEW_TOUCHING_POS + self.EDGES_TOUCHING_POS:
            edge = edges[index]
            edge.set_opacity(1)
            self._transform_points(edge.points, +self.COHESIVE_OFFSET)
        for index in self.EDGES_TOUCHING_NEG:
            edge = edges[index]
            self._transform_points(edge.points, -self.COHESIVE_OFFSET)
        for index in self.EDGES_IMPINGING_POS:
            edge = edges[index]
            edge.set_opacity(1)
            self._transform_points(edge.points, +self.COHESIVE_OFFSET)
        for index in self.EDGES_IMPINGING_NEG:
            edge = edges[index]
            self._transform_points(edge.points, -self.COHESIVE_OFFSET)
        return edges

    def _transform_vertices(self):
        vertices = [vertex.copy() for vertex in self.vertices]
        for vertex in vertices:
            vertex.set(color=self.COLOR_VERTEX)
        for index in self.VERTICES_SPLIT_NEG:
            vertex = vertices[index]
            vertex.set_opacity(1)
            vertex.move_to((vertex.get_x(), vertex.get_y() - self.COHESIVE_OFFSET, vertex.get_z()))
        for index in self.VERTICES_NEW:
            vertex = vertices[index]
            vertex.set_opacity(1)
            vertex.move_to((vertex.get_x(), vertex.get_y() + self.COHESIVE_OFFSET, vertex.get_z()))
        return vertices


class Animation(manim.Scene):

    def construct(self):
        self.domain = Domain()
        self.mesh = Mesh()

        self.domain.display(self)
        self.wait(1.0)

        self.mesh.discretize(self)
        self.wait(1.0)

        self.mesh.mark_fault(self)
        self.wait(1.0)

        self.mesh.orient_fault(self)
        self.wait(1.0)

        self.mesh.i_step = 3
        self.mesh.label_fault_points(self)
        self.wait(1.0)

        self.mesh.set_transform_ops(self)
        self.wait(1.0)

        self.mesh.transform_topology(self)
        self.wait(1.0)

        self.mesh.update_petscsf(self)
        self.wait(1.0)
