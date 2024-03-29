from baam.keyboard.constants import KC, _______


name = "BAAMboard-prototype"

"""
  ┌───┐   ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┐
  │Esc│   │F1 │F2 │F3 │F4 │ │F5 │F6 │F7 │F8 │ │F9 │F10│F11│F12│ │PSc│Scr│Pse│
  └───┘   └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┘
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐ ┌───┬───┬───┐ ┌───┬───┬───┬───┐
  │ ` │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ = │ Backsp│ │Ins│Hom│PgU│ │Num│ / │ * │ - │
  ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤ ├───┼───┼───┤ ├───┼───┼───┼───┤
  │ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │ [ │ ] │  \  │ │Del│End│PgD│ │ 7 │ 8 │ 9 │   │
  ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤ └───┴───┴───┘ ├───┼───┼───┤ + │
  │ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │ ' │  Enter │               │ 4 │ 5 │ 6 │   │
  ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤     ┌───┐     ├───┼───┼───┼───┤
  │ Shift  │ Z │ X │ C │ V │ B │ N │ M │ , │ . │ / │    Shift │     │ ↑ │     │ 1 │ 2 │ 3 │   │
  ├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤ ┌───┼───┼───┐ ├───┴───┼───┤Ent│
  │Ctrl│GUI │Alt │                        │ Alt│ GUI│Menu│Ctrl│ │ ← │ ↓ │ → │ │   0   │ . │   │
  └────┴────┴────┴────────────────────────┴────┴────┴────┴────┘ └───┴───┴───┘ └───────┴───┴───┘

"""


#  Row: 0     1        2        3      4      5      6       7      8      9        10       11       12       13       14       15     */
layers = {
    "base": (
        (
            KC.ESC,
            KC.F1,
            KC.F2,
            KC.F3,
            KC.F4,
            KC.F5,
            KC.F6,
            KC.F7,
            KC.F8,
            KC.F9,
            KC.F10,
            KC.F11,
            KC.F12,
            KC.PSCR,
            KC.SCRL,
            KC.PAUS,
        ),
        (
            KC.GRV,
            KC.N1,
            KC.N2,
            KC.N3,
            KC.N4,
            KC.N5,
            KC.N6,
            KC.N7,
            KC.N8,
            KC.N9,
            KC.N0,
            KC.MINS,
            KC.EQL,
            KC.BSPC,
            KC.INS,
            KC.HOME,
            KC.PGUP,
            KC.NUM,
            KC.PSLS,
            KC.PAST,
            KC.PMNS,
        ),
        (
            KC.TAB,
            KC.Q,
            KC.W,
            KC.E,
            KC.R,
            KC.T,
            KC.Y,
            KC.U,
            KC.I,
            KC.O,
            KC.P,
            KC.LBRC,
            KC.RBRC,
            KC.BSLS,
            KC.DEL,
            KC.END,
            KC.PGDN,
            KC.P7,
            KC.P8,
            KC.P9,
            KC.PPLS,
        ),
        (
            KC.CAPS,
            KC.A,
            KC.S,
            KC.D,
            KC.F,
            KC.G,
            KC.H,
            KC.J,
            KC.K,
            KC.L,
            KC.SCLN,
            KC.QUOT,
            KC.ENT,
            KC.P4,
            KC.P5,
            KC.P6,
        ),
        (
            KC.LSFT,
            KC.Z,
            KC.X,
            KC.C,
            KC.V,
            KC.B,
            KC.N,
            KC.M,
            KC.COMM,
            KC.DOT,
            KC.SLSH,
            KC.RSFT,
            KC.UP,
            KC.P1,
            KC.P2,
            KC.P3,
            KC.PENT,
        ),
        (
            KC.LCTL,
            KC.LGUI,
            KC.LALT,
            KC.SPC,
            KC.RALT,
            KC.RGUI,
            KC.APP,
            KC.RCTL,
            KC.LEFT,
            KC.DOWN,
            KC.RGHT,
            KC.P0,
            KC.PDOT,
        ),
    )
}
