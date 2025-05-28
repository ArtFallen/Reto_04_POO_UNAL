import math

class Point:
    def __init__(self, x_pos: int, y_pos: int):
        self.x = x_pos
        self.y = y_pos

    def distance_to(self, other):
        # Calcula la distancia euclidiana entre dos puntos
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

class Line:
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point
        self.length = self.start.distance_to(self.end)

class Shape:
    def __init__(self, is_regular=False):
        self.is_regular = is_regular
        self.vertices = []
        self.edges = []
        self.angles = []

    def set_vertices(self, points_list):
        self.vertices = points_list

    def set_edges(self, lines_list):
        self.edges = lines_list

    def set_angles(self, angles_list):
        self.angles = angles_list

    def area(self):
        # Método base, se sobrescribe en clases hijas
        return None

    def perimeter(self):
        total = 0
        for edge in self.edges:
            total += edge.length
        return total

    def inner_angles(self):
        # Método base, se sobrescribe en clases hijas
        return None

class Rectangle(Shape):
    def __init__(self, init_type, *args):
        super().__init__(is_regular=False)
        if init_type == 1:
            bottom_left, width, height = args
            self.width = width
            self.height = height
            self.center = Point(bottom_left.x + width/2, bottom_left.y + height/2)
        elif init_type == 2:
            center, width, height = args
            self.width = width
            self.height = height
            self.center = center
        elif init_type == 3:
            p1, p2 = args
            self.width = abs(p2.x - p1.x)
            self.height = abs(p2.y - p1.y)
            self.center = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
        self._build_shape()

    def _build_shape(self):
        left = self.center.x - self.width/2
        right = self.center.x + self.width/2
        bottom = self.center.y - self.height/2
        top = self.center.y + self.height/2
        bl = Point(left, bottom)
        br = Point(right, bottom)
        tr = Point(right, top)
        tl = Point(left, top)
        self.set_vertices([bl, br, tr, tl])
        e1 = Line(bl, br)
        e2 = Line(br, tr)
        e3 = Line(tr, tl)
        e4 = Line(tl, bl)
        self.set_edges([e1, e2, e3, e4])
        self.set_angles([90, 90, 90, 90])

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def inner_angles(self):
        return [90, 90, 90, 90]

    def contains_point(self, pt: Point):
        left = self.center.x - self.width/2
        right = self.center.x + self.width/2
        bottom = self.center.y - self.height/2
        top = self.center.y + self.height/2
        return left <= pt.x <= right and bottom <= pt.y <= top

    def intersects_line(self, p1: Point, p2: Point):
        # Para simplificar, verificamos si algún extremo de la línea está dentro del rectángulo
        if self.contains_point(p1) or self.contains_point(p2):
            return True
        return False

class Square(Rectangle):
    def __init__(self, center: Point, side_length: float):
        super().__init__(2, center, side_length, side_length)
        self.is_regular = True

class Triangle(Shape):
    def __init__(self, point1: Point, point2: Point, point3: Point):
        super().__init__(is_regular=False)
        self.set_vertices([point1, point2, point3])
        l1 = Line(point1, point2)
        l2 = Line(point2, point3)
        l3 = Line(point3, point1)
        self.set_edges([l1, l2, l3])
        self.angles = self.inner_angles()

    def inner_angles(self):
        a = self.edges[0].length
        b = self.edges[1].length
        c = self.edges[2].length
        # Usamos ley del coseno para calcular ángulos
        angle1 = math.degrees(math.acos((b*b + c*c - a*a) / (2 * b * c)))
        angle2 = math.degrees(math.acos((a*a + c*c - b*b) / (2 * a * c)))
        angle3 = 180 - angle1 - angle2
        return [angle1, angle2, angle3]

    def area(self):
        a, b, c = [edge.length for edge in self.edges]
        s = (a + b + c) / 2
        area_val = s * (s - a) * (s - b) * (s - c)
        if area_val > 0:
            return math.sqrt(area_val)
        else:
            return 0

class Isosceles(Triangle):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__(p1, p2, p3)
        lengths = [edge.length for edge in self.edges]
        # Dos lados iguales indica isósceles
        self.is_regular = lengths.count(lengths[0]) == 2 or lengths.count(lengths[1]) == 2

class Equilateral(Triangle):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__(p1, p2, p3)
        lengths = [round(edge.length, 5) for edge in self.edges]
        # Todos los lados iguales indica equilátero
        self.is_regular = all(l == lengths[0] for l in lengths)

class Scalene(Triangle):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__(p1, p2, p3)
        lengths = [edge.length for edge in self.edges]
        # Todos los lados diferentes indica escaleno
        self.is_regular = len(set(lengths)) == 3

class RightTriangle(Triangle):
    def __init__(self, p1: Point, p2: Point, p3: Point):
        super().__init__(p1, p2, p3)
        angles_rounded = [round(angle, 5) for angle in self.angles]
        # Al menos un ángulo de 90 grados indica triángulo rectángulo
        self.is_regular = any(abs(angle - 90) < 1e-3 for angle in angles_rounded)
