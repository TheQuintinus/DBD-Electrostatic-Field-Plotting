import pyvista as pv

import field


class Plot:
    """
    PyVista plot of the electric field using fixed-size glyphs and magnitude-based coloring.
    """

    def __init__(self, glyph_size=1e-3):
        """
        Initialize the PyVista plotter and field model.

        Parameters
        ----------
        glyph_size : float, optional
            Length of the glyphs representing the electric field vectors.
            The glyph size is fixed and does not scale with field magnitude.
        """

        self.glyph_size = glyph_size
        self.field = field.DielectricField()
        self.plotter = pv.Plotter()

    def show(self):
        """
        Render the electric field visualization.

        The method computes the electric field, creates a point cloud,
        attaches vector and magnitude data, and renders oriented glyphs
        colored by field magnitude.

        Returns
        -------
        None
        """

        points, vectors_unit, mag = self.field.calculate_field()

        cloud = pv.PolyData(points)
        cloud["vectors"] = vectors_unit
        cloud["mag"] = mag

        glyphs = cloud.glyph(orient="vectors", scale=False, factor=self.glyph_size)

        self.plotter.add_mesh(
            glyphs,
            scalars="mag",
            cmap="viridis",
            scalar_bar_args={"title": "|E| [V/m]"},
        )

        self.plotter.add_axes()
        self.plotter.show()
