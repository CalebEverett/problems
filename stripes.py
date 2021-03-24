from functools import partial

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from typing import Tuple

df = pd.read_csv("to_stripe.tsv", sep="\t")


class ColorSetter:
    """Sets alternating row colors for changes in values in up to two columns. Can be called with
    alternate_rows flag set to True to altenate dark and light shading every other row regardless of values.
    Takes up to two column names and two colors. If only one column and color provided, will
    alternate light and dark colors with changes in value in single column. If two columns
    are provided, will alternate color shades on changes in value in first column and alternate
    dark and light based on changes in value in second column.

    Attributes:
        df: Dataframe on which to apply color scheme.
        columns: Names of datframe columns on which to base alternating
            colors.
        colors: Base color for rows to colored with darker shade.
        lighter_pct: Percent lighter than base color for rows to be colored
            with lighter shade.

    """

    def __init__(
        self,
        df: DataFrame,
        columns: Tuple[str],
        colors: Tuple[Tuple],
        lighter_pct: float = 0.80,
    ):
        self.df = df.copy()
        self.columns = columns
        self.colors = colors
        self.lighter_pct = lighter_pct

        if not set(columns).issubset(set(df.columns)):
            raise IndexError("Specified columns not found in Dataframe.")

        if len(self.columns) != len(self.colors):
            raise Exception("Must have same number of colors as columns.")

        if len(self.columns) > 2:
            raise Exception("Number of columns must be less than or equal to 2.")

    def get_color(self, indicators: Tuple = (0, 0)) -> Tuple:
        """Gets color of row based on mod of cumulative changes in value as provided
        in indicators.

        Args:
            indicators[0]: Cumulative number of changes in group value for secondary
                group. Used to alternate between lighter and darker shades of same
                color.
            indicators[1]: Cumulative number of changes in group value for primary
                group. Used to change color.
        """
        indicator_0, indicator_1 = indicators
        color = np.array(self.colors[indicator_1 % 2])
        white = np.array([255, 255, 255])
        vector = white - color
        lighter_pct = self.lighter_pct * (indicator_0 % 2)
        return tuple((color + vector * lighter_pct).astype(int))

    def get_indicator(self, idx: int) -> Series:
        """Return cumulative total of number of value changes in column at
        idx of self.columns.
        """
        shifted_col = (
            self.df[self.columns[idx]].shift().fillna(df[self.columns[idx]].iloc[0])
        )
        return (shifted_col != self.df[self.columns[idx]]).cumsum()

    def alternate_groups(self):
        """Alternates row colors based on up to two groups."""
        if len(self.columns) == 1:
            self.df["COLOR"] = self.get_indicator(0).map(
                lambda x: self.get_color((x, 0))
            )
        else:
            self.df["COLOR"] = Series(
                map(self.get_color, zip(*map(self.get_indicator, (1, 0))))
            )

    def alternate_rows(self):
        """Alternates light and dark color every other row."""
        self.df["COLOR"] = df.index.map(lambda x: self.get_color((x, 0)))

    def __call__(self, alternate_rows: bool = False) -> DataFrame:
        if alternate_rows:
            self.alternate_rows()
        else:
            self.alternate_groups()

        return self.df


colors = ((240, 200, 80), (80, 200, 240))
columns = ("REP", "CITY")

df_colored = ColorSetter(df, columns, colors)()


def main():
    print(df_colored.head(60))


if __name__ == "__main__":
    main()
