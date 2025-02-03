from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
import japanize_kivy
import random
import joblib
import pandas as pd

# 学習済みモデルとラベルエンコーダーをロード
try:
    model = joblib.load("game_cpu_model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    model = None
    label_encoder = None

def intelligent_cpu_action(hand, opponent_hand):
    """
    学習済みモデルを使ってCPUのアクションを決定
    """
    if not model or not label_encoder:
        # モデルがロードされていない場合、ランダムに行動
        return random.choice(["A→a", "B→b", "C→c"])

    features = {
        "player1_a": opponent_hand.get("a", 0),
        "player1_b": opponent_hand.get("b", 0),
        "player1_c": opponent_hand.get("c", 0),
        "player2_a": hand.get("A", 0),
        "player2_b": hand.get("B", 0),
        "player2_c": hand.get("C", 0),
    }
    df_features = pd.DataFrame([features])
    try:
        prediction = model.predict(df_features)
        action = label_encoder.inverse_transform(prediction)[0]
    except Exception as e:
        print(f"モデルエラー: {e}")
        action = random.choice(["A→a", "B→b", "C→c"])
    return action


class FingerGameScreen_1_A(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file("namoaso_2.kv")  # kvファイルの正確な名前を指定

    def on_enter(self):
        self.init_game()
        self.update_font_size()  # 初期フォントサイズを設定
        Window.bind(size=self.update_font_size)  # 画面サイズ変更時にフォントサイズを更新

    def update_font_size(self, *args):
        base_size = min(Window.width, Window.height) * 0.05  # 全体の5%を基準とする
        self.ids.timer_label_1.font_size = base_size * 1.5
        self.ids.timer_label_2.font_size = base_size * 1.5
        self.ids.status_label_1.font_size = base_size * 1.0
        self.ids.status_label_2.font_size = base_size * 1.0
        self.ids.next_button_1.font_size = base_size * 1.0
        self.ids.next_button_2.font_size = base_size * 1.0

    def init_game(self):
        # ゲームの初期化
        self.turn = random.randint(1, 2)
        self.o = random.randint(1, 3)
        self.p = random.randint(1, 3)
        self.q = random.randint(1, 3)
        self.r = random.randint(1, 3)
        
        # 不正な組み合わせの回避
        if self.o == 3 and self.q == 2:
            self.o = random.randint(1, 2)
        if self.o == 2 and self.q == 3:
            self.q = random.randint(1, 2)
        if self.o == 3 and self.r == 2:
            self.o = random.randint(1, 2)
        if self.o == 2 and self.r == 3:
            self.r = random.randint(1, 2)
        if self.p == 3 and self.q == 2:
            self.p = random.randint(1, 2)
        if self.p == 2 and self.q == 3:
            self.q = random.randint(1, 2)
        if self.p == 3 and self.r == 2:
            self.p = random.randint(1, 2)
        if self.p == 2 and self.r == 3:
            self.r = random.randint(1, 2)

        # 初期手の設定
        self.hand_1 = {'a': 1, 'b': self.o, 'c': self.p}
        self.hand_2 = {'A': 1, 'B': self.q, 'C': self.r}
        self.timer_seconds = 15
        self.selected_input_1 = None
        self.selected_input_2 = None
        
        # 初回のターンタイマーを開始
        self.update_hand_display()
        self.start_timer()
        
    def start_timer(self):
        if self.turn == 1:
            self.ids.status_label_1.text = "あなたのターン"
            self.ids.status_label_2.text = "相手のターン"
            Clock.unschedule(self.update_timer_2)
            Clock.schedule_interval(self.update_timer_1, 1)
            self.ids.next_button_2.disabled = True
        else:
            self.ids.status_label_1.text = "相手のターン"
            self.ids.status_label_2.text = "あなたのターン"
            Clock.unschedule(self.update_timer_1)
            Clock.schedule_interval(self.update_timer_2, 1)
            self.ids.next_button_1.disabled = True
            Clock.schedule_once(self.cpu_turn, 3)

    def update_timer_1(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.ids.timer_label_1.text = f"{self.timer_seconds}"
        else:
            self.ids.status_label_1.text = "タイムアップ！\nあなたの負けです"
            self.ids.status_label_2.text = "相手の勝ちです"
            Clock.unschedule(self.update_timer_1)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True

    def update_timer_2(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.ids.timer_label_2.text = f"{self.timer_seconds}"
        else:
            self.ids.status_label_1.text = "相手の負けです"
            self.ids.status_label_2.text = "タイムアップ！\nあなたの勝ちです"
            Clock.unschedule(self.update_timer_2)
            self.ids.next_button_1.disabled = True
            self.ids.next_button_2.disabled = True

    def on_image_tap_1(self, image_id):
    
        if self.turn != 1:  # プレイヤーのターンでない場合は何もしない
            return

        # 以前の選択をリセット
        if self.selected_input_1:
            previous_id = self.selected_input_1
            if previous_id in self.hand_1:
                self.ids[f"player1_{previous_id}"].background_normal = f"hand_{self.hand_1[previous_id]}.png"

        # 新しい選択を記録
        self.selected_input_1 = image_id

        # 新しい選択をハイライト
        if image_id in self.hand_1:
            self.ids[f"player1_{image_id}"].background_normal = f"hand_{self.hand_1[image_id]}_select.png"

    def on_image_tap_2(self, image_id):
    
        if self.turn != 1:  # プレイヤーのターンでない場合は何もしない
            return

        # 以前の選択をリセット
        if self.selected_input_2:
            previous_id = self.selected_input_2
            if previous_id in self.hand_2:
                self.ids[f"player2_{previous_id}"].background_normal = f"hand_{self.hand_2[previous_id]}.png"

        # 新しい選択を記録
        self.selected_input_2 = image_id

        # 新しい選択をハイライト
        if image_id in self.hand_2:
            self.ids[f"player2_{image_id}"].background_normal = f"hand_{self.hand_2[image_id]}_select.png"

        # プレイヤーのターンの入力が完了した場合
        if self.selected_input_1 and self.selected_input_2:
            self.process_turn()
    
    def process_turn(self):
    
        if self.turn == 1:  # プレイヤーのターン
            player_input_1 = self.selected_input_1  # プレイヤーの攻撃元
            player_input_2 = self.selected_input_2  # プレイヤーの攻撃先
            if player_input_1 in self.hand_1 and player_input_2 in self.hand_2:
                # 指の本数を加算
                self.hand_2[player_input_2] += self.hand_1[player_input_1]
                if self.hand_2[player_input_2] > 4:
                    self.hand_2[player_input_2] %= 5
                if self.hand_2[player_input_2] == 0:  # 指が0になった場合
                    del self.hand_2[player_input_2]

            # ターンをCPUに切り替える
            self.turn = 2
            self.selected_input_1 = None
            self.selected_input_2 = None
            self.update_hand_display()
            self.timer_seconds = 15
            self.start_timer()

            # CPUの行動をスケジュール
            Clock.schedule_once(self.cpu_turn, 2)  # 2秒後にCPUの行動開始
    
    def next_turn(self):
        if self.timer_seconds <= 0 or not self.selected_input_1 or not self.selected_input_2:
            return
        if self.turn == 1:
            player_input_1 = self.selected_input_1
            player_input_2 = self.selected_input_2
            if player_input_1 in self.hand_1 and player_input_2 in self.hand_2:
                self.hand_2[player_input_2] += self.hand_1[player_input_1]
                if self.hand_2[player_input_2] > 4:
                    self.hand_2[player_input_2] %= 5
                if self.hand_2[player_input_2] == 0:
                    del self.hand_2[player_input_2]
            self.turn = 2
        else:
            Clock.schedule_once(self.cpu_turn, 1)  # CPUの行動
            return
        self.update_hand_display()
        self.timer_seconds = 15
        self.start_timer()

    def cpu_turn(self, *args):
    
        action = intelligent_cpu_action(self.hand_2, self.hand_1)  # CPUの行動を決定
        cpu_key, target_key = action.split("→")  # 攻撃元と攻撃先を取得

        # 指の本数を加算
        if cpu_key in self.hand_2 and target_key in self.hand_1:
            self.hand_1[target_key] += self.hand_2[cpu_key]
            if self.hand_1[target_key] > 4:
                self.hand_1[target_key] %= 5
            if self.hand_1[target_key] == 0:  # 指が0になった場合
                del self.hand_1[target_key]

        # ターンをプレイヤーに切り替える
        self.turn = 1
        self.selected_input_1 = None
        self.selected_input_2 = None
        self.update_hand_display()
        self.timer_seconds = 15
        self.start_timer()

    def update_hand_display(self):
        for key in self.hand_1:
            try:
                self.ids[f"player1_{key}"].background_normal = f"hand_{self.hand_1[key]}.png"
            except KeyError:
                pass
        for key in self.hand_2:
            try:
                self.ids[f"player2_{key}"].background_normal = f"hand_{self.hand_2[key]}.png"
            except KeyError:
                pass