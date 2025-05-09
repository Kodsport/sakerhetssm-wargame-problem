package main

import "database/sql"

func createAdminNotes(db *sql.DB) error {
	_, err := db.Exec("INSERT INTO notes (id, user_id, note) VALUES ('first', 'admin', 'first flag part SSM{skuggade_vars_');")
	if err != nil {
		return err
	}
	_, err = db.Exec("INSERT INTO notes (id, user_id, note) VALUES ('second', 'admin', 'second flag part farliga_vars}');")
	if err != nil {
		return err
	}

	return nil
}
