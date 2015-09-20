class CreateTweets < ActiveRecord::Migration
  def change
    create_table :tweets do |t|
      t.string :tweet
      t.string :username
      t.float :sentiment
      t.datetime :tweeted_at
      t.string :party

      t.timestamps null: false
    end
  end
end
